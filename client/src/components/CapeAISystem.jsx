import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import CapeAIFloatingButton from './CapeAIFloatingButton';
import OnboardingFlow from './onboarding/OnboardingFlow';
import useOnboarding from '../hooks/useOnboarding';
import useCapeAI from '../hooks/useCapeAI';

export default function CapeAISystem() {
  const location = useLocation();
  
  // Add error boundary for context usage
  let onboardingData, capeAIData;
  
  try {
    onboardingData = useOnboarding();
    capeAIData = useCapeAI();
  } catch (error) {
    console.warn('CapeAI context not available:', error);
    return null; // Don't render if context is not available
  }
  
  const { currentStep, showContextualHelp, isComplete } = onboardingData;
  const { addMessage, isVisible } = capeAIData;

  // Handle route-based contextual messages
  useEffect(() => {
    if (!isComplete) {
      const routeMessages = {
        '/dashboard': 'Welcome to your dashboard! This is where you can monitor and manage all your AI agents.',
        '/profile': 'Let\'s get your profile set up! This helps me provide better assistance tailored to your business.',
        '/agents': 'Ready to explore AI agents? I can help you find the perfect agent for your needs.',
        '/settings': 'Need help with settings? I can guide you through the configuration options.',
        '/features': 'Let me show you our amazing platform features and how they can benefit your business!'
      };

      const message = routeMessages[location.pathname];
      if (message && !isVisible) {
        // Delay the message slightly to avoid spam
        const timer = setTimeout(() => {
          addMessage('assistant', message);
        }, 2000);
        
        return () => clearTimeout(timer);
      }
    }
  }, [location.pathname, isComplete, isVisible, addMessage]);

  // Auto-suggest help for new users
  useEffect(() => {
    if (!isComplete && currentStep === 'welcome') {
      const welcomeTimer = setTimeout(() => {
        showContextualHelp('welcome');
      }, 3000); // Show welcome after 3 seconds

      return () => clearTimeout(welcomeTimer);
    }
  }, [currentStep, isComplete, showContextualHelp]);

  return (
    <>
      {/* Main floating chat interface */}
      <CapeAIFloatingButton />
      
      {/* Onboarding flow manager */}
      {!isComplete && <OnboardingFlow />}
    </>
  );
}
