import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { StarIcon, QuoteIcon } from "lucide-react";

export default function Hero() {
  const navigate = useNavigate();

  return (
    <section className="text-center py-20 px-4 bg-gradient-to-b from-white to-blue-50">
      <h1 className="text-4xl sm:text-5xl font-extrabold text-blue-700 mb-6 leading-tight">
        Empower Your Business with AI Agents—<br className="hidden sm:inline" />
        <span className="text-blue-600">Fast, Affordable, and Simple.</span>
      </h1>

      <p className="text-gray-600 max-w-xl mx-auto mb-8">
        Access a curated library of AI-driven tools to automate tasks, boost productivity,
        and grow your business—no coding required.
      </p>

      <div className="flex justify-center gap-4 mb-10">
        <Button onClick={() => navigate("/register")}>Try for Free</Button>
        <Button variant="outline" onClick={() => navigate("/how-it-works")}>See How It Works</Button>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-xl shadow-md mx-auto w-full max-w-4xl overflow-hidden"
      >
        <img
          src="/static/dashboard-preview.png"
          alt="Dashboard preview"
          className="w-full h-auto"
          loading="lazy"
        />
        <div className="py-2 text-sm text-gray-700 font-medium">Dashboard preview</div>
      </motion.div>

      <div className="mt-8 text-gray-500 text-sm flex justify-center items-center gap-2">
        <StarIcon className="w-4 h-4 text-yellow-500" />
        Trusted by 1,200+ freelancers and small businesses
      </div>

      <div className="mt-10 max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md text-gray-700 italic">
        <QuoteIcon className="w-6 h-6 text-blue-500 mx-auto mb-2" />
        “CapeControl helped us streamline our workflow in ways we didn’t think possible.
        The AI tools feel like extra team members!”
        <div className="mt-2 text-right text-sm font-medium">— Alex M., Founder of SmartEdge</div>
      </div>
    </section>
  );
}
