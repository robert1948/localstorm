import { useState } from "react";
import { useNavigate } from "react-router-dom";

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

// Help Support Component
function HelpSupport() {
  return (
    <div className="text-center mt-6">
      <a 
        href="#" 
        className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 transition-colors"
        onClick={(e) => {
          e.preventDefault();
          // You can integrate with your support system here
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

// Step 1: Basic Registration Component
function BasicRegistration({ onNext, formData, setFormData }) {
  const [email, setEmail] = useState(formData.email || "");
  const [password, setPassword] = useState(formData.password || "");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [firstName, setFirstName] = useState(formData.firstName || "");
  const [lastName, setLastName] = useState(formData.lastName || "");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Validation
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters long");
      return;
    }

    // Update form data and proceed to next step
    setFormData({
      ...formData,
      email,
      password,
      firstName,
      lastName,
    });

    onNext();
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-8 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-6">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Create Account</h2>
        <p className="text-gray-600">Step 1: Basic Information</p>
        <ProgressBar currentStep={1} totalSteps={3} />
      </div>

      {error && <p className="text-red-600 text-sm mb-4 text-center bg-red-50 p-3 rounded">{error}</p>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              First Name
            </label>
            <input
              type="text" autoComplete="username"
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Last Name
            </label>
            <input
              type="text" autoComplete="username"
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Email Address
          </label>
          <input
            type="email" autoComplete="username"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Password
          </label>
          <input
            type="password" autoComplete="new-password"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Confirm Password
          </label>
          <input
            type="password" autoComplete="new-password"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
        >
          Continue
        </button>
      </form>

      <p className="text-center text-sm text-gray-600 mt-4">
        Already have an account?{" "}
        <a href="/login" className="text-blue-600 hover:underline">
          Sign in
        </a>
      </p>
      
      <HelpSupport />
    </div>
  );
}

// Step 2: Role Selection Component
function RoleSelection({ onNext, formData, setFormData }) {
  const [selectedRole, setSelectedRole] = useState(formData.role || "");

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
    setFormData({
      ...formData,
      role,
    });
  };

  const handleNext = () => {
    if (selectedRole) {
      onNext();
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-20 p-8 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Choose Your Role</h2>
        <p className="text-gray-600">Step 2: Select how you'll use CapeControl</p>
        <ProgressBar currentStep={2} totalSteps={3} />
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-8">
        {/* User Role */}
        <div
          className={`border-2 rounded-lg p-6 cursor-pointer transition-all ${
            selectedRole === "user"
              ? "border-blue-500 bg-blue-50"
              : "border-gray-300 hover:border-gray-400"
          }`}
          onClick={() => handleRoleSelect("user")}
        >
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <svg className="w-12 h-12 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">User</h3>
            <p className="text-gray-600 text-sm">
              I want to use AI agents to automate tasks and boost productivity for my business.
            </p>
            <ul className="text-left text-sm text-gray-600 mt-4 space-y-1">
              <li>• Access pre-built AI agents</li>
              <li>• Automate business processes</li>
              <li>• No coding required</li>
              <li>• Easy-to-use dashboard</li>
            </ul>
          </div>
        </div>

        {/* Developer Role */}
        <div
          className={`border-2 rounded-lg p-6 cursor-pointer transition-all ${
            selectedRole === "developer"
              ? "border-blue-500 bg-blue-50"
              : "border-gray-300 hover:border-gray-400"
          }`}
          onClick={() => handleRoleSelect("developer")}
        >
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <svg className="w-12 h-12 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/>
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Developer</h3>
            <p className="text-gray-600 text-sm">
              I want to create and sell AI agents on the CapeControl marketplace.
            </p>
            <ul className="text-left text-sm text-gray-600 mt-4 space-y-1">
              <li>• Build custom AI agents</li>
              <li>• Sell on the marketplace</li>
              <li>• Access developer tools</li>
              <li>• Revenue sharing program</li>
            </ul>
          </div>
        </div>
      </div>

      <button
        onClick={handleNext}
        disabled={!selectedRole}
        className={`w-full p-3 rounded-lg font-semibold transition-colors ${
          selectedRole
            ? "bg-blue-600 text-white hover:bg-blue-700"
            : "bg-gray-300 text-gray-500 cursor-not-allowed"
        }`}
      >
        Continue to Details
      </button>
      
      <HelpSupport />
    </div>
  );
}

// Step 3: Detailed Information Component
function DetailedRegistration({ formData, setFormData, onSubmit }) {
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

    setLoading(true);
    setError("");

    const finalData = {
      ...formData,
      company,
      phone,
      website,
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
    <div className="max-w-md mx-auto mt-20 p-8 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-6">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Complete Registration</h2>
        <p className="text-gray-600">
          Step 3: {formData.role === "user" ? "Business" : "Developer"} Details
        </p>
        <ProgressBar currentStep={3} totalSteps={3} />
      </div>

      {error && <p className="text-red-600 text-sm mb-4 text-center bg-red-50 p-3 rounded">{error}</p>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {formData.role === "user" ? "Company Name" : "Developer/Company Name"}
          </label>
          <input
            type="text" autoComplete="username"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
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
            {formData.role === "user" ? "Business Experience" : "Development Experience"}
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

        <div className="flex items-start space-x-3">
          <input
            type="checkbox"
            id="terms"
            className="mt-1"
            checked={agreedToTerms}
            onChange={(e) => setAgreedToTerms(e.target.checked)}
          />
          <label htmlFor="terms" className="text-sm text-gray-600">
            I agree to the{" "}
            <a href="/terms" className="text-blue-600 hover:underline" target="_blank">
              Terms & Conditions
            </a>{" "}
            for {formData.role === "user" ? "Users" : "Developers"}
          </label>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full p-3 rounded-lg font-semibold transition-colors ${
            loading
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

// Main Registration Component
export default function Register() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({});
  const navigate = useNavigate();

  const handleNext = () => {
    setCurrentStep(currentStep + 1);
  };

  const handleSubmit = async (finalData) => {
    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(finalData),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Registration failed");
      }

      const userData = await res.json();

      // Registration successful - redirect to Phase 2 based on role
      if (finalData.role === "user") {
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
        <BasicRegistration
          onNext={handleNext}
          formData={formData}
          setFormData={setFormData}
        />
      )}
      {currentStep === 2 && (
        <RoleSelection
          onNext={handleNext}
          formData={formData}
          setFormData={setFormData}
        />
      )}
      {currentStep === 3 && (
        <DetailedRegistration
          formData={formData}
          setFormData={setFormData}
          onSubmit={handleSubmit}
        />
      )}
    </div>
  );
}
