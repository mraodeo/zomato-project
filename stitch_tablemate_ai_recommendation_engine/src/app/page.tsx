"use client";

import { useState } from "react";

export default function Home() {
  const [formData, setFormData] = useState({
    location: "BTM Layout", // Match select option value exactly
    cuisine: "North Indian",
    budget: "medium", 
    min_rating: 3.5, 
    family_friendly: true,
    top_n: 5,
  });
  
  // Convert boolean toggle to text string for API
  const finalFormData = {
    ...formData,
    additional_preferences: formData.family_friendly ? "Family-friendly" : "",
  };

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState("");

  const handleChange = (e: any) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : (type === "range" ? Number(value) : value),
    }));
  };

  const handleBudgetChange = (val: string) => {
    setFormData((prev) => ({ ...prev, budget: val }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError("");
    setResults(null);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${API_URL}/api/v1/recommendations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(finalFormData),
      });
      if (!response.ok) throw new Error("Failed to fetch recommendations.");
      const data = await response.json();
      setResults(data);
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col font-sans text-textPrimary selection:bg-accent selection:text-white">
      {/* Header */}
      <header className="border-b border-borderLight bg-background sticky top-0 z-50">
        <div className="max-w-[1440px] mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            {/* Logo icon */}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 4L20 20M4 20L20 4" stroke="#ff4f5e" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <h1 className="text-2xl font-bold tracking-tight text-white ml-2">TableMate AI</h1>
          </div>
          
          <nav className="hidden md:flex gap-8">
            <a href="#" className="text-white font-medium border-b-2 border-accent pb-1">Explore</a>
            <a href="#" className="text-textSecondary hover:text-white transition-colors">My List</a>
            <a href="#" className="text-textSecondary hover:text-white transition-colors">Reservations</a>
            <a href="#" className="text-textSecondary hover:text-white transition-colors">Concierge</a>
          </nav>
          
          <div className="flex items-center gap-5 text-textSecondary">
            <button className="hover:text-white transition-colors"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg></button>
            <button className="hover:text-white transition-colors"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg></button>
            <div className="w-8 h-8 rounded-full bg-borderLight border border-surface overflow-hidden">
               {/* Placeholder avatar */}
               <div className="w-full h-full bg-surface" />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-[1440px] mx-auto w-full px-6 py-8 flex-1 grid grid-cols-1 lg:grid-cols-[400px_1fr] gap-10 items-start">
        
        {/* LEFT PANEL: Form */}
        <aside className="bg-panel rounded-xl p-8 shadow-2xl sticky top-28">
          <h2 className="text-3xl font-extrabold mb-8 leading-tight text-white tracking-tight">What are you in the mood for?</h2>
          
          <div className="space-y-8">
            {/* Location */}
            <div>
              <label className="block text-[11px] font-bold text-textSecondary uppercase tracking-wider mb-2">Location</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-textSecondary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                </div>
                <select
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  className="w-full bg-background border border-borderLight rounded-lg pl-10 pr-10 py-3 focus:outline-none focus:border-accent text-white appearance-none cursor-pointer"
                >
                  <option value="BTM Layout">BTM Layout, Bangalore</option>
                  <option value="Jayanagar">Jayanagar, Bangalore</option>
                  <option value="Koramangala">Koramangala, Bangalore</option>
                  <option value="Indiranagar">Indiranagar, Bangalore</option>
                  <option value="Banashankari">Banashankari, Bangalore</option>
                  <option value="Basavanagudi">Basavanagudi, Bangalore</option>
                  <option value="JP Nagar">JP Nagar, Bangalore</option>
                  <option value="Whitefield">Whitefield, Bangalore</option>
                  <option value="Marathahalli">Marathahalli, Bangalore</option>
                  <option value="HSR Layout">HSR Layout, Bangalore</option>
                </select>
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-textSecondary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                </div>
              </div>
            </div>

            {/* Budget segmented control */}
            <div>
              <label className="block text-[11px] font-bold text-textSecondary uppercase tracking-wider mb-2">Budget for Two</label>
              <div className="flex rounded-lg border border-borderLight bg-background overflow-hidden p-1">
                {['low', 'medium', 'high'].map((b) => (
                  <button
                    key={b}
                    type="button"
                    onClick={() => handleBudgetChange(b)}
                    className={`flex-1 py-2 text-sm font-medium capitalize rounded-md transition-colors ${formData.budget === b ? 'bg-accent text-white' : 'text-textSecondary hover:text-white hover:bg-surface'}`}
                  >
                    {b}
                  </button>
                ))}
              </div>
            </div>

            {/* Cuisines pills */}
            <div>
              <label className="block text-[11px] font-bold text-textSecondary uppercase tracking-wider mb-3">Cuisines (Optional)</label>
              <div className="flex flex-wrap gap-2">
                {['North Indian', 'South Indian', 'Chinese'].map((c) => {
                  const isActive = formData.cuisine === c;
                  return (
                    <button
                      key={c}
                      onClick={() => setFormData(prev => ({ ...prev, cuisine: isActive ? "" : c }))}
                      className={`px-4 py-1.5 rounded-full border text-sm font-medium flex items-center gap-1 transition-colors ${
                        isActive 
                          ? 'border-accent bg-accent/10 text-accent' 
                          : 'border-borderLight text-textSecondary hover:text-white hover:border-textSecondary'
                      }`}
                    >
                      {c} {isActive && <svg className="w-3.5 h-3.5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>}
                    </button>
                  );
                })}
                <button 
                  onClick={() => setFormData(prev => ({ ...prev, cuisine: "" }))}
                  className="px-4 py-1.5 rounded-full border border-borderLight text-textSecondary hover:text-white hover:border-textSecondary text-sm font-medium flex items-center gap-1"
                >
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"></path></svg> Any
                </button>
              </div>
            </div>

            {/* Minimum Rating */}
            <div>
              <div className="flex justify-between items-center mb-4">
                <label className="block text-xs font-bold text-textSecondary uppercase tracking-wider">Minimum Rating</label>
                <span className="text-sm font-bold text-accent">{formData.min_rating}+</span>
              </div>
              <input
                type="range"
                name="min_rating"
                min="0"
                max="5"
                step="0.1"
                value={formData.min_rating}
                onChange={handleChange}
                className="w-full mb-2"
              />
              <div className="flex justify-between text-[10px] text-textSecondary uppercase tracking-wider font-bold">
                <span>Any</span>
                <span>5.0</span>
              </div>
            </div>

            {/* Checkbox */}
            <div className="flex items-center gap-3 pt-2">
              <div className="relative flex items-center">
                <input
                  type="checkbox"
                  name="family_friendly"
                  checked={formData.family_friendly}
                  onChange={handleChange}
                  className="w-5 h-5 appearance-none border border-borderLight rounded bg-background checked:bg-accent checked:border-accent transition-colors cursor-pointer"
                />
                <svg className={`absolute left-1 w-3 h-3 text-white pointer-events-none transition-opacity ${formData.family_friendly ? 'opacity-100' : 'opacity-0'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg>
              </div>
              <span className="text-white font-medium">Family-friendly</span>
            </div>

            {/* Submit Button */}
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="w-full mt-8 py-3.5 bg-accent hover:bg-accentHover text-white text-base font-bold rounded-lg transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing
                </span>
              ) : (
                "Get Recommendations"
              )}
            </button>
          </div>
        </aside>

        {/* RIGHT PANEL: Results */}
        <div className="w-full pb-20">
          
          {/* Error Message */}
          {error && (
            <div className="mb-8 p-4 bg-red-900/20 border border-accent/50 rounded-xl text-accent">
              {error}
            </div>
          )}

          {/* Intro state */}
          {!results && !loading && !error && (
             <div className="h-64 flex items-center justify-center border-2 border-dashed border-borderLight rounded-xl text-textSecondary">
               Click 'Get Recommendations' to see AI matches.
             </div>
          )}

          {/* Results State */}
          {results && (
            <div className="animate-in fade-in slide-in-from-bottom-4">
              
              {/* AI Match Complete Banner */}
              {results.summary && (
                <div className="mb-8">
                  <h3 className="text-sm font-bold text-textSecondary uppercase tracking-wider mb-2">AI Match Complete</h3>
                  <p className="text-white italic text-lg opacity-90">{results.summary}</p>
                  <p className="text-xs text-textSecondary mt-2 tracking-wide uppercase">Matches Found in the Area</p>
                </div>
              )}

              <div className="space-y-6">
                {results.recommendations?.map((rec: any, idx: number) => (
                  <div key={idx} className="bg-panel border border-borderLight/50 rounded-xl overflow-hidden hover:border-borderLight transition-colors">
                    
                    <div className="p-6">
                      <div className="flex justify-between items-start mb-1">
                        <div className="flex items-center gap-3">
                           {/* Rating Pill */}
                           <div className="flex items-center gap-1.5 bg-background border border-borderLight px-2.5 py-1 rounded-md">
                             <svg className="w-3.5 h-3.5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                             <span className="font-bold text-sm text-white">{rec.rating.toFixed(1)}</span>
                           </div>
                           <h4 className="text-2xl font-bold text-white">{rec.restaurant_name}</h4>
                        </div>
                        {/* Bookmark Icon */}
                        <button className="text-textSecondary hover:text-white p-1">
                          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
                        </button>
                      </div>

                      <p className="text-sm font-medium text-textSecondary mb-6 pl-14">
                        {rec.cuisine} • {formData.location.split(',')[0]} • ₹{rec.estimated_cost} for two
                      </p>

                      <div className="bg-surface rounded-lg p-4 border border-borderLight/30 ml-14">
                        <p className="text-sm text-textSecondary leading-relaxed">
                          <strong className="text-white font-semibold">AI Match: </strong>
                          {rec.explanation}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
