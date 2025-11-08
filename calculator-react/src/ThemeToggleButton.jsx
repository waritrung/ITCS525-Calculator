import { useContext } from "react";
import { ThemeContext } from "./ThemeContext";
import toggleIcon from "./assets/theme.png";

export default function ThemeToggleButton() {
  const { darkMode, setDarkMode } = useContext(ThemeContext);

  return (
    <button
      onClick={() => setDarkMode(prev => !prev)}
      className="absolute top-4 right-4 w-60 h-20 bg-gray-200 dark:bg-gray-800 rounded-full flex items-center justify-center shadow-md hover:scale-105 transition"
      title="Toggle Theme"
    >
      <img
        src={toggleIcon}
        alt="Toggle Theme"
        className="w-40 h-40 object-contain"
      />
    </button>
  );
}
