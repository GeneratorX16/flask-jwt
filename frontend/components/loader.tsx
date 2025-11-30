import { Loader } from 'lucide-react';

const LoadingSpinner = () => {
  return (
    <div className="flex items-center justify-center h-screen">
      <Loader className="animate-slowSpin w-12 h-12 text-blue-500" /> {/* Using custom animation */}
    </div>
  );
};

export default LoadingSpinner;