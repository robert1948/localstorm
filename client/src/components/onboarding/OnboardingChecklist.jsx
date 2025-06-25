export default function OnboardingChecklist() {
  const checklist = [
    { label: "✅ Set up your profile", done: true },
    { label: "📄 Review the platform features", done: false },
    { label: "🤖 Meet your AI assistant", done: false },
    { label: "📈 View your dashboard", done: true },
    { label: "🚀 Launch your first agent", done: false },
  ];

  return (
    <div className="bg-white p-6 rounded-lg shadow mt-6">
      <h3 className="text-lg font-semibold mb-4">Getting Started Checklist</h3>
      <ul className="space-y-2">
        {checklist.map((item, index) => (
          <li
            key={index}
            className={`flex items-center gap-2 ${
              item.done ? "text-green-600" : "text-gray-800"
            }`}
          >
            <span className="text-xl">{item.done ? "✔️" : "⬜"}</span>
            {item.label}
          </li>
        ))}
      </ul>
    </div>
  );
}
