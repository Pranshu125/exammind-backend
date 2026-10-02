import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import { ArrowRight, BrainCircuit, Target, CheckCircle2 } from 'lucide-react';

export default function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { signup, loginWithGoogle } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    if (password !== confirmPassword) {
      return setError('Passwords do not match.');
    }
    try {
      setError('');
      setLoading(true);
      await signup(email, password);
      navigate('/');
    } catch {
      setError('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  async function handleGoogleSignIn() {
    try {
      setError('');
      setLoading(true);
      await loginWithGoogle();
      navigate('/');
    } catch {
      setError('Google authentication failed.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen w-full flex flex-col md:flex-row bg-[#FAFAFA]">
      
      {/* Left Side - Brand & Graphics (Hidden on Mobile) */}
      <div className="hidden md:flex md:w-1/2 lg:w-[55%] bg-[#141A21] text-white p-12 lg:p-20 flex-col justify-between relative overflow-hidden">
        <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-blue-500/10 blur-[120px] rounded-full pointer-events-none -translate-x-1/2 -translate-y-1/2"></div>
        
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-16">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg">
              <BrainCircuit className="text-white" size={24} />
            </div>
            <span className="text-2xl font-bold tracking-tight">EXAMMIND</span>
          </div>

          <h1 className="text-4xl lg:text-5xl xl:text-6xl font-bold leading-[1.1] tracking-tight mb-8">
            Start building your <br/><span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">perfect study plan.</span>
          </h1>
          
          <div className="space-y-6 mt-12 max-w-lg">
            <div className="flex items-start gap-4">
              <CheckCircle2 className="text-green-400 mt-1 shrink-0" size={20} />
              <div>
                <h3 className="font-bold text-gray-200">Instant Syllabus parsing</h3>
                <p className="text-gray-400 text-sm mt-1 leading-relaxed">Drop your PDF and get a complete module breakdown instantly.</p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <CheckCircle2 className="text-green-400 mt-1 shrink-0" size={20} />
              <div>
                <h3 className="font-bold text-gray-200">Adaptive Revision</h3>
                <p className="text-gray-400 text-sm mt-1 leading-relaxed">Dynamic notes and quizzes generated specifically for your weak points.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Form */}
      <div className="w-full md:w-1/2 lg:w-[45%] flex items-center justify-center p-6 sm:p-12 lg:p-16 relative">
        <div className="w-full max-w-[420px] space-y-8">
          
          <div className="md:hidden flex items-center gap-3 mb-10">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg">
              <BrainCircuit className="text-white" size={24} />
            </div>
            <span className="text-2xl font-bold tracking-tight text-gray-900">EXAMMIND</span>
          </div>

          <div>
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 mb-2">Create an account</h2>
            <p className="text-gray-500 font-medium">Join thousands of students studying smarter.</p>
          </div>
          
          {error && (
            <div className="bg-red-50 text-red-700 p-4 rounded-xl text-sm font-medium border border-red-100 flex items-center gap-3">
              <div className="w-1.5 h-1.5 rounded-full bg-red-600"></div>
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-1.5">
              <label className="text-sm font-semibold text-gray-700">Email address</label>
              <input type="email" required placeholder="name@school.edu" onChange={e => setEmail(e.target.value)} />
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-semibold text-gray-700">Password</label>
              <input type="password" required placeholder="Create a strong password" onChange={e => setPassword(e.target.value)} />
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-semibold text-gray-700">Confirm Password</label>
              <input type="password" required placeholder="Repeat password" onChange={e => setConfirmPassword(e.target.value)} />
            </div>
            
            <div className="pt-2">
              <button disabled={loading} type="submit" className="btn-primary w-full h-12 text-base">
                Create Account <ArrowRight size={18} />
              </button>
            </div>
          </form>
          
          <div className="relative py-2">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-200"></div>
            </div>
            <div className="relative flex justify-center">
              <span className="bg-[#FAFAFA] px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">Or register with</span>
            </div>
          </div>
          
          <button disabled={loading} onClick={handleGoogleSignIn} className="btn-base w-full h-12 text-base">
            <svg className="w-5 h-5 mr-1" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
            </svg>
            Google
          </button>
          
          <div className="pt-6 text-center text-sm font-medium text-gray-500">
            Already have an account? <Link to="/login" className="text-black hover:text-blue-600 transition-colors ml-1">Log in</Link>
          </div>
        </div>
      </div>
    </div>
  );
}