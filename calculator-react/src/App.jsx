import { useEffect, useState } from "react";
import toggleIcon from "./assets/theme.png";
import Button from "./Button";
import { useContext } from "react";
import ThemeToggleButton from "./ThemeToggleButton";

export default function App() {
  const [input, setInput] = useState("0");
  const [history, setHistory] = useState([]);
  const [triggerHistoryReload, setTriggerHistoryReload] = useState(0);

  const fetchHistory = async () => {
    const rootAPI = "http://localhost:8000";
    try {
      const res = await fetch(`${rootAPI}/history`);
      const data = await res.json();
      console.log("✅ Backend returned:", data);
      
      // Check for expected format
      if (Array.isArray(data)) {
        setHistory(data);
      } else if (data?.history && Array.isArray(data.history)) {
        setHistory(data.history);
      } else {
        console.warn("⚠️ Unexpected history format", data);
      }
    } catch (err) {
      console.error("❌ Failed to fetch history:", err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [triggerHistoryReload]);

  const handleClick = (value) => {
    const rootAPI = "http://localhost:8000";

    if (value === "AC") {
      setInput("0");
      return;
    }

    if (value === "⌫") {
      if (input === "Error") {
        setInput("0");
      } else {
        setInput(input.length === 1 ? "0" : input.slice(0, -1));
      }
      return;
    }

    if (value === "=") {
      const expr = input.replaceAll("÷", "/").replaceAll("×", "*").replaceAll("−", "-");

      fetch(`${rootAPI}/calculate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expr })
      })
        .then(res => res.json())
        .then(data => {
          if (data.ok) {
            const result = data.result.toString();
            setInput(result);

            // Optional: log to history
            fetch(`${rootAPI}/history`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                expr: data.expr,
                result: data.result,
                ok: true,
                error: ""
              })
            }).finally(() => {
              setTriggerHistoryReload(prev => prev + 1);
            });
          } else {
            setInput("Error");
          }
        })
        .catch((err) => {
          console.error("❌ Calculation failed:", err);
          setInput("Error");
        });

      return;
    }

    // Default case: append numbers or operators
    setInput((prev) => (prev === "0" || prev === "Error" ? value : prev + value));
  };


  const handleClearHistoryClick = () => {
    const rootAPI = "http://localhost:8000";
    
    // Fire and forget
    fetch(`${rootAPI}/history`, { method: "DELETE" })
      .finally(() => {
        setTriggerHistoryReload(prev => prev + 1);
      });
  };


  const topRow = ["⌫", "AC", "%", "÷"];
  const rows = [
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["±", "0", ".", "="],
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
    {/* Theme toggle button in top-right corner */}
    <ThemeToggleButton />
    {/* Flex container for history and calculator side-by-side */}
    <div className="flex space-x-6 items-start">
      {/* History Panel */}
      <div className="bg-white dark:bg-black text-black dark:text-white rounded-3xl p-4 shadow-2xl w-80 h-[500px] flex flex-col">
        <h2 className="text-2xl font-light mb-3 text-right">History</h2>

        <div className="flex-1 overflow-y-auto bg-gray-200 dark:bg-gray-800 rounded-xl p-3 text-right">
          {history.length === 0 ? (
            <p className="text-gray-500 italic">No history</p>
          ) : (
            history.map((item, idx) => (
              <div key={idx} className="mb-2 text-lg">
                {item.expr} = {item.result}
              </div>
            ))
          )}
        </div>

        <button
          onClick={handleClearHistoryClick}
          className="mt-4 text-sm text-red-400 underline hover:text-red-600 self-end"
        >
          Clear History
        </button>
      </div>

      {/* Calculator Panel */}
      <div className="bg-white dark:bg-black text-black dark:text-white rounded-3xl p-4 shadow-2xl w-80">
        {/* Display */}
        <div className="text-right text-5xl font-light p-4 mb-2">
          {input}
        </div>

        {/* Top Row */}
        <div className="grid grid-cols-4 gap-3 mb-3">
          {topRow.map((btn) => (
            <button
              key={btn}
              onClick={() => handleClick(btn)}
              className="bg-gray-300 dark:bg-gray-600 text-black dark:text-white text-2xl rounded-full w-16 h-16 flex items-center justify-center hover:opacity-80"
            >
              {btn}
            </button>
          ))}
        </div>

        {/* Number/Operator Rows */}
        {rows.map((row, i) => (
          <div key={i} className="grid grid-cols-4 gap-3 mb-3">
            {row.map((btn) => {
              const isOperator = ["÷", "×", "−", "+", "="].includes(btn);
              return (
                <button
                  key={btn}
                  onClick={() => handleClick(btn)}
                  className={`${
                    isOperator
                      ? "bg-orange-500 text-white"
                      : "bg-gray-300 dark:bg-gray-700 text-black dark:text-white"
                  } text-2xl rounded-full flex items-center justify-center hover:opacity-80 w-16 h-16`}
                >
                  {btn}
                </button>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  </div>
);



}