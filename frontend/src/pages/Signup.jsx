import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

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
    <div className="flex min-h-screen font-sans bg-[#f4f4f0] text-[#111]">
      <div className="flex w-full max-w-6xl mx-auto my-0 md:my-12 eink-card md:shadow-2xl overflow-hidden">
        
        {/* Left Side: Editorial */}
        <div className="hidden lg:flex w-1/2 border-r border-gray-300 p-16 flex-col justify-between">
          <div>
            <h1 className="text-6xl font-serif font-black tracking-tighter uppercase mb-8">EXAMMIND.</h1>
            <h2 className="text-3xl font-serif italic text-gray-700 mb-8 leading-relaxed">
              "Clarity of mind through rigorous organization."
            </h2>
            <div className="h-px w-24 bg-black mb-8"></div>
            <p className="font-serif text-lg text-gray-600 leading-loose">
              Join scholars worldwide who have abandoned chaotic planning. A minimalist, AI-driven study planner designed for absolute focus.
            </p>
          </div>
          <div className="text-sm font-bold uppercase tracking-widest text-gray-500">
            Subscription Application
          </div>
        </div>

        {/* Right Side: Form */}
        <div className="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-16 bg-white">
          <div className="w-full max-w-sm">
            
            <div className="text-left mb-12 lg:hidden">
              <h1 className="text-4xl font-serif font-black tracking-tighter uppercase">EXAMMIND.</h1>
            </div>
            
            <h2 className="text-2xl font-serif font-bold mb-8">Create Subscription</h2>
            
            {error && (
              <div className="border border-black p-4 mb-8 text-sm font-bold flex items-start gap-3 bg-gray-50">
                <span>!</span> <span className="font-serif">{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-xs font-bold uppercase tracking-widest text-gray-500 mb-2">Email Address</label>
                <input type="email" required onChange={e => setEmail(e.target.value)} />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-widest text-gray-500 mb-2">Password</label>
                <input type="password" required onChange={e => setPassword(e.target.value)} />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-widest text-gray-500 mb-2">Confirm Password</label>
                <input type="password" required onChange={e => setConfirmPassword(e.target.value)} />
              </div>
              <div className="pt-4">
                <button disabled={loading} type="submit" className="w-full eink-btn-primary uppercase tracking-widest text-sm">
                  Subscribe <ArrowRight size={16} />
                </button>
              </div>
            </form>
            
            <div className="my-10 flex items-center justify-center relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <span className="relative bg-white px-4 text-xs font-bold text-gray-400 uppercase tracking-widest italic font-serif">or via</span>
            </div>
            
            <button disabled={loading} onClick={handleGoogleSignIn} className="w-full eink-btn uppercase tracking-widest text-sm">
              <svg className="w-4 h-4 mr-3 grayscale" viewBox="0 0 24 24">
                <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
              </svg>
              Google
            </button>
            
            <div className="mt-12 pt-8 border-t border-gray-200 text-center">
              <span className="text-sm font-serif text-gray-500">
                Already subscribed? <Link to="/login" className="text-black font-bold hover:underline ml-1">Sign In</Link>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
