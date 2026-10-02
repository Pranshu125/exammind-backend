export function requestNotificationPermission() {
  if ('Notification' in window) {
    if (Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }
}

export function scheduleStudyAlerts(studyPlan) {
  if (!('Notification' in window) || Notification.permission !== 'granted') return;
  
  // For demonstration purposes, we schedule the first day's alerts a few seconds from now,
  // and subsequent days incrementally. In a production app, this would use a Service Worker 
  // or check exact timestamps.
  
  studyPlan.days?.forEach((day, index) => {
    const delay = (index * 60000) + 5000; // 5s for day 1, 65s for day 2...
    
    setTimeout(() => {
      new Notification(`Study Reminder: Day ${day.day}`, {
        body: `Topics to cover: ${day.topics_to_cover.join(', ')}`,
      });
    }, delay);
  });
}
