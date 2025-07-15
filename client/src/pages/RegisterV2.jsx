import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { validateEmail, validatePassword, registerUserV2 } from "../api/auth";

// Progress Bar Component
function ProgressBar({ currentStep, totalSteps }) {
  const progress = (currentStep / totalSteps) * 100;
  
  return (
    <div className="w-full bg-gray-200 rounded-full h-2 mt-4">
      <div 
        className="bg-blue-600 h-2 rounded-full transition-all duration-300 ease-in-out" 
        style={{ width: `${progress}%` }}
      ></div>
    </div>
  );
}

// Password Strength Indicator
function PasswordStrengthIndicator({ password }) {
  const calculateStrength = (pwd) => {
    let score = 0;
    if (pwd.length >= 12) score += 25;
    if (/[a-z]/.test(pwd)) score += 25;
    if (/[A-Z]/.test(pwd)) score += 25;
    if (/[0-9]/.test(pwd)) score += 15;
    if (/[^A-Za-z0-9]/.test(pwd)) score += 10;
    return Math.min(score, 100);
  };

  const strength = calculateStrength(password);
  const getStrengthLabel = () => {
    if (strength < 30) return { label: "Weak", color: "bg-red-500" };
    if (strength < 60) return { label: "Fair", color: "bg-yellow-500" };
    if (strength < 80) return { label: "Good", color: "bg-blue-500" };
    return { label: "Strong", color: "bg-green-500" };
  };

  const { label, color } = getStrengthLabel();

  if (!password) return null;

  return (
    <div className="mt-2">
      <div className="flex justify-between text-xs text-gray-600 mb-1">
        <span>Password Strength</span>
        <span>{label}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-1">
        <div 
          className={`h-1 rounded-full transition-all duration-300 ${color}`}
          style={{ width: `${strength}%` }}
        ></div>
      </div>
    </div>
  );
}

// Email Validation Indicator
function EmailValidationIndicator({ email, isValid, isChecking }) {
  if (!email) return null;
  
  return (
    <div className="mt-1 text-xs flex items-center">
      {isChecking ? (
        <>
          <div className="animate-spin h-3 w-3 border border-blue-500 rounded-full border-t-transparent mr-2"></div>
          <span className="text-gray-500">Checking availability...</span>
        </>
      ) : isValid === true ? (
        <>
          <svg className="h-3 w-3 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          <span className="text-green-600">✓ Email available</span>
        </>
      ) : isValid === false ? (
        <>
          <svg className="h-3 w-3 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
          <span className="text-red-600">Email already registered</span>
        </>
      ) : null}
    </div>
  );
}

// Role Selection Card Component
function RoleCard({ role, selectedRole, onSelect }) {
  const isSelected = selectedRole === role;
  const roleData = {
    customer: {
      title: "Customer",
      icon: "👤",
      description: "Access pre-built AI agents to automate business processes. No coding required.",
      features: [
        "Ready-to-use AI agents",
        "Business process automation", 
        "Easy-to-use dashboard",
        "No technical knowledge needed"
      ],
      color: "blue"
    },
    developer: {
      title: "Developer", 
      icon: "👨‍💻",
      description: "Build custom AI agents with developer tools. Earn 30% revenue share.",
      features: [
        "Build custom AI agents",
        "30% revenue sharing",
        "Developer tools & APIs",
        "Marketplace publishing"
      ],
      color: "purple"
    }
  };

  const data = roleData[role];
  const colorClasses = {
    blue: {
      border: isSelected ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-blue-300",
      icon: "text-blue-600",
      title: "text-blue-700",
      features: "text-blue-600"
    },
    purple: {
      border: isSelected ? "border-purple-500 bg-purple-50" : "border-gray-300 hover:border-purple-300", 
      icon: "text-purple-600",
      title: "text-purple-700",
      features: "text-purple-600"
    }
  };

  const colors = colorClasses[data.color];

  return (
    <div
      className={`border-2 rounded-lg p-6 cursor-pointer transition-all ${colors.border}`}
      onClick={() => onSelect(role)}
    >
      <div className="text-center">
        <div className={`text-4xl mb-3 ${colors.icon}`}>
          {data.icon}
        </div>
        <h3 className={`text-xl font-semibold mb-2 ${colors.title}`}>
          {data.title}
        </h3>
        <p className="text-gray-600 text-sm mb-4">
          {data.description}
        </p>
        <ul className="text-left text-sm space-y-1">
          {data.features.map((feature, index) => (
            <li key={index} className={`${colors.features}`}>
              • {feature}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

// Help Support Component
function HelpSupport() {
  return (
    <div className="text-center mt-6">
      <a 
        href="#" 
        className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 transition-colors"
        onClick={(e) => {
          e.preventDefault();
          alert("Support chat would open here. Contact: support@capecontrol.com");
        }}
      >
        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Need Help?
      </a>
    </div>
  );
}

// Step 1: Basic Information + Role Selection (New 2-Step Flow)
function BasicInfoAndRole({ onNext, formData, setFormData }) {
  const [firstName, setFirstName] = useState(formData.firstName || "");
  const [lastName, setLastName] = useState(formData.lastName || "");
  const [email, setEmail] = useState(formData.email || "");
  const [password, setPassword] = useState(formData.password || "");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [selectedRole, setSelectedRole] = useState(formData.role || "");
  const [error, setError] = useState("");
  
  // Real-time validation states
  const [emailValid, setEmailValid] = useState(null);
  const [emailChecking, setEmailChecking] = useState(false);
  const [passwordMatch, setPasswordMatch] = useState(true);

  // Password validation
  const validatePassword = (pwd) => {
    const requirements = {
      minLength: pwd.length >= 12,
      hasUpper: /[A-Z]/.test(pwd),
      hasLower: /[a-z]/.test(pwd),
      hasNumber: /[0-9]/.test(pwd),
      hasSpecial: /[^A-Za-z0-9]/.test(pwd)
    };
    
    return {
      isValid: Object.values(requirements).every(Boolean),
      requirements
    };
  };

  // Real-time email validation
  useEffect(() => {
    const validateEmailAvailability = async () => {
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        setEmailValid(null);
        return;
      }

      setEmailChecking(true);
      try {
        const result = await validateEmail(email);
        setEmailValid(result.available);
      } catch (error) {
        console.error('Email validation error:', error);
        setEmailValid(null);
      } finally {
        setEmailChecking(false);
      }
    };

    const debounce = setTimeout(validateEmailAvailability, 500);
    return () => clearTimeout(debounce);
  }, [email]);

  // Real-time password match validation
  useEffect(() => {
    if (confirmPassword) {
      setPasswordMatch(password === confirmPassword);
    }
  }, [password, confirmPassword]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Enhanced validation
    if (!firstName.trim() || !lastName.trim()) {
      setError("First and last name are required");
      return;
    }

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError("Please enter a valid email address");
      return;
    }

    if (emailValid === false) {
      setError("This email is already registered. Try logging in or use a different email.");
      return;
    }

    const passwordValidation = validatePassword(password);
    if (!passwordValidation.isValid) {
      setError("Password must be at least 12 characters with uppercase, lowercase, number, and special character");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (!selectedRole) {
      setError("Please select your role");
      return;
    }

    // Update form data and proceed to next step
    setFormData({
      ...formData,
      firstName: firstName.trim(),
      lastName: lastName.trim(),
      email: email.trim().toLowerCase(),
      password,
      role: selectedRole,
    });

    onNext();
  };

  const passwordValidation = validatePassword(password);

  return (
    <div className="max-w-4xl mx-auto mt-10 p-8 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Create Your CapeControl Account</h2>
        <p className="text-gray-600">Step 1: Basic Information & Role Selection</p>
        <ProgressBar currentStep={1} totalSteps={2} />
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm text-center">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Personal Information */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Personal Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                First Name *
              </label>
              <input
                type="text" autoComplete="username"
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="Enter your first name"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Last Name *
              </label>
              <input
                type="text" autoComplete="username"
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Enter your last name"
                required
              />
            </div>
          </div>
        </div>

        {/* Account Information */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Information</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email Address *
              </label>
              <input
                type="email" autoComplete="username"
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email address"
                required
              />
              <EmailValidationIndicator 
                email={email} 
                isValid={emailValid} 
                isChecking={emailChecking} 
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password *
              </label>
              <input
                type="password" autoComplete="new-password"
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Create a strong password"
                minLength={12}
                required
              />
              <PasswordStrengthIndicator password={password} />
              {password && (
                <div className="mt-2 text-xs text-gray-600">
                  <p className="font-medium">Password Requirements:</p>
                  <ul className="mt-1 space-y-1">
                    <li className={passwordValidation.requirements.minLength ? 'text-green-600' : 'text-red-600'}>
                      ✓ At least 12 characters
                    </li>
                    <li className={passwordValidation.requirements.hasUpper ? 'text-green-600' : 'text-red-600'}>
                      ✓ One uppercase letter
                    </li>
                    <li className={passwordValidation.requirements.hasLower ? 'text-green-600' : 'text-red-600'}>
                      ✓ One lowercase letter
                    </li>
                    <li className={passwordValidation.requirements.hasNumber ? 'text-green-600' : 'text-red-600'}>
                      ✓ One number
                    </li>
                    <li className={passwordValidation.requirements.hasSpecial ? 'text-green-600' : 'text-red-600'}>
                      ✓ One special character
                    </li>
                  </ul>
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Confirm Password *
              </label>
              <input
                type="password" autoComplete="new-password"
                className={`w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  confirmPassword && !passwordMatch ? 'border-red-300' : 'border-gray-300'
                }`}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm your password"
                required
              />
              {confirmPassword && !passwordMatch && (
                <p className="mt-1 text-xs text-red-600">Passwords do not match</p>
              )}
              {confirmPassword && passwordMatch && (
                <p className="mt-1 text-xs text-green-600">Passwords match ✓</p>
              )}
            </div>
          </div>
        </div>

        {/* Role Selection */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Choose Your Role</h3>
          <p className="text-gray-600 mb-6">Select how you'll use CapeControl to get personalized features</p>
          
          <div className="grid md:grid-cols-2 gap-6">
            <RoleCard 
              role="customer" 
              selectedRole={selectedRole} 
              onSelect={setSelectedRole} 
            />
            <RoleCard 
              role="developer" 
              selectedRole={selectedRole} 
              onSelect={setSelectedRole} 
            />
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-6">
          <button
            type="submit"
            className="w-full bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 transition-colors font-semibold text-lg disabled:bg-gray-400 disabled:cursor-not-allowed"
            disabled={emailChecking || !passwordMatch || !passwordValidation.isValid || !selectedRole}
          >
            {emailChecking ? "Checking email..." : "Continue to Details →"}
          </button>
          
          {(!passwordValidation.isValid || !passwordMatch || !selectedRole) && (
            <p className="text-center text-xs text-gray-500 mt-2">
              {!passwordValidation.isValid && "Complete password requirements, "}
              {!passwordMatch && "confirm password, "}
              {!selectedRole && "select your role "}
              to continue
            </p>
          )}
        </div>

        <p className="text-center text-sm text-gray-600 mt-4">
          Already have an account?{" "}
          <a href="/login-customer" className="text-blue-600 hover:underline">
            Sign in
          </a>
        </p>
      </form>
      
      <HelpSupport />
    </div>
  );
}

// Step 2: Detailed Information (Role-specific)
function DetailedInformation({ formData, setFormData, onSubmit }) {
  const [company, setCompany] = useState(formData.company || "");
  const [phone, setPhone] = useState(formData.phone || "");
  const [website, setWebsite] = useState(formData.website || "");
  const [experience, setExperience] = useState(formData.experience || "");
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!agreedToTerms) {
      setError("You must agree to the Terms & Conditions");
      return;
    }

    if (!company.trim()) {
      setError("Company/Organization name is required");
      return;
    }

    setLoading(true);
    setError("");

    const finalData = {
      ...formData,
      company: company.trim(),
      phone: phone.trim(),
      website: website.trim(),
      experience,
    };

    try {
      await onSubmit(finalData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 p-8 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Complete Your Profile</h2>
        <p className="text-gray-600">
          Step 2: {formData.role === "customer" ? "Business" : "Developer"} Details
        </p>
        <ProgressBar currentStep={2} totalSteps={2} />
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm text-center">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {formData.role === "customer" ? "Company Name" : "Developer/Company Name"} *
          </label>
          <input
            type="text"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            placeholder={formData.role === "customer" ? "Your company name" : "Your name or company"}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Phone Number
          </label>
          <input
            type="tel"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="+1 (555) 123-4567"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Website (Optional)
          </label>
          <input
            type="url"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={website}
            onChange={(e) => setWebsite(e.target.value)}
            placeholder="https://"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {formData.role === "customer" ? "Business Experience" : "Development Experience"} *
          </label>
          <select
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={experience}
            onChange={(e) => setExperience(e.target.value)}
            required
          >
            <option value="">Select experience level</option>
            <option value="beginner">Beginner (0-1 years)</option>
            <option value="intermediate">Intermediate (2-5 years)</option>
            <option value="advanced">Advanced (5+ years)</option>
            <option value="expert">Expert (10+ years)</option>
          </select>
        </div>

        <div className="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg">
          <input
            type="checkbox"
            id="terms"
            className="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            checked={agreedToTerms}
            onChange={(e) => setAgreedToTerms(e.target.checked)}
          />
          <label htmlFor="terms" className="text-sm text-gray-700">
            I agree to the{" "}
            <a href="/terms" className="text-blue-600 hover:underline" target="_blank">
              Terms & Conditions
            </a>{" "}
            and{" "}
            <a href="/privacy" className="text-blue-600 hover:underline" target="_blank">
              Privacy Policy
            </a>{" "}
            for {formData.role === "customer" ? "Users" : "Developers"}
          </label>
        </div>

        <button
          type="submit"
          disabled={loading || !agreedToTerms}
          className={`w-full p-4 rounded-lg font-semibold text-lg transition-colors ${
            loading || !agreedToTerms
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          } text-white`}
        >
          {loading ? "Creating Account..." : "Create Account"}
        </button>
      </form>
      
      <HelpSupport />
    </div>
  );
}

// Main Registration Component (New 2-Step Flow)
export default function Register() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({});
  const navigate = useNavigate();

  const handleNext = () => {
    setCurrentStep(currentStep + 1);
  };

  const handleSubmit = async (finalData) => {
    try {
      const userData = await registerUserV2(finalData);

      // Registration successful - redirect to Phase 2 based on role
      if (finalData.role === "customer") {
        navigate("/phase2-customer", { 
          state: { userData: { ...finalData, ...userData } }
        });
      } else {
        navigate("/phase2-developer", { 
          state: { userData: { ...finalData, ...userData } }
        });
      }
    } catch (err) {
      throw err;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      {currentStep === 1 && (
        <BasicInfoAndRole
          onNext={handleNext}
          formData={formData}
          setFormData={setFormData}
        />
      )}
      {currentStep === 2 && (
        <DetailedInformation
          formData={formData}
          setFormData={setFormData}
          onSubmit={handleSubmit}
        />
      )}
    </div>
  );
}
