import { Link } from "react-router-dom";
const BrandAnalysis = () => {
  return (
    <div className="bg-[#0f0e17] text-[#fffffe] h-screen flex-col justify-center mx-auto items-center">
      <Link to="/">
        <h1 className="text-3xl font-bold py-6 ml-10">SponsorBuzz</h1>
      </Link>
      <h1 className="text-3xl font-bold py-3 text-center ml-10">
        Brand Analysis
      </h1>
      <iframe
        className="w-full max-w-2xl mx-auto pt-10"
        width="650"
        height="500"
        src="https://www.youtube.com/embed/t_9hPrBuSu8"
        title="Vsideo player"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      ></iframe>
      <button className="mt-4 px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 mx-auto text-center flex">
        Download
      </button>
    </div>
  );
};

export default BrandAnalysis;
