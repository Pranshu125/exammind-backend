import { collection, getDocs } from 'firebase/firestore';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { db, storage } from './firebase';

export const generateAndUploadWebcal = async (currentUser) => {
  if (!currentUser) return null;
  try {
    const examsSnap = await getDocs(collection(db, `users/${currentUser.uid}/exams`));
    
    let icsContent = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Exammind//Master Schedule//EN\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:Exammind Timetable\n";

    examsSnap.forEach(doc => {
      const exam = doc.data();
      if (!exam.schedule) return;
      
      exam.schedule.forEach(day => {
        if(!day.date) return;
        const dateParts = day.date.split('-');
        if(dateParts.length !== 3) return;
        
        const year = dateParts[0];
        const month = dateParts[1].padStart(2, '0');
        const date = dateParts[2].padStart(2, '0');
        let currentHour = 9;

        day.tasks?.forEach((task, tIdx) => {
          const startHour = String(currentHour).padStart(2, '0');
          const startMin = "00";
          const durationMins = task.estimated_minutes || 60;
          const endHour = String(currentHour + Math.floor(durationMins / 60)).padStart(2, '0');
          const endMin = String(durationMins % 60).padStart(2, '0');

          icsContent += "BEGIN:VEVENT\n";
          icsContent += `DTSTART:${year}${month}${date}T${startHour}${startMin}00\n`;
          icsContent += `DTEND:${year}${month}${date}T${endHour}${endMin}00\n`;
          icsContent += `SUMMARY:[${task.task_type}] ${task.subject}: ${task.topic}\n`;
          icsContent += `DESCRIPTION:Exammind AI Generated Study Session\n`;
          icsContent += "END:VEVENT\n";

          currentHour += Math.floor(durationMins / 60) + 1;
        });
      });
    });
    icsContent += "END:VCALENDAR";

    const storageRef = ref(storage, `calendars/${currentUser.uid}.ics`);
    await uploadBytes(storageRef, new Blob([icsContent], { type: 'text/calendar' }));
    const downloadURL = await getDownloadURL(storageRef);
    
    // Convert https to webcal
    const webcalReady = downloadURL.replace(/^https?:\/\//i, 'webcal://');
    return webcalReady;
  } catch (err) {
    console.error("Failed to generate master ICS:", err);
    return null;
  }
};
