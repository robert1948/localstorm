import MainLayout from "../components/layout/MainLayout";
import OnboardingChecklist from "../components/onboarding/OnboardingChecklist";

export default function Dashboard() {
  return (
    <MainLayout>
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
        <p className="text-gray-700">Welcome to your CapeControl dashboard.</p>

        <OnboardingChecklist />
      </div>
    </MainLayout>
  );
}
