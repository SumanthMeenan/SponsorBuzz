import { Routes, Route } from "react-router-dom";
import BrandAnalysis from "./Home/BrandAnalysis";
import Home from "./Home/Home";
import Vplayer from "./Home/Vplayer";
const App = () => {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route path="/player" element={<Vplayer />}></Route>
        <Route path="/brandanalysis" element={<BrandAnalysis />}></Route>
      </Routes>
    </div>
  );
};

export default App;
