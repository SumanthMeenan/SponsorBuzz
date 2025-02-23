import Upload from "../assets/upload.svg";
import { Link } from "react-router-dom";
const Home = () => {
  return (
    <div className="bg-[#0f0e17] text-[#fffffe] h-screen flex-col justify-center">
      <div className="flex flex-col mx-auto">
        <h1 className="text-3xl font-bold my-6 ml-10">SponsorBuzz</h1>

        <div className="mb-6 flex-col justify-center border border-gray-300 p-5 rounded-lg shadow-lg w-3/4 mx-auto">
          <img src={Upload} alt="" className="w-[250px] mx-auto mb-10" />
          <input
            type="file"
            accept="video/*"
            id="file-upload"
            className="hidden"
          />
          <label
            htmlFor="file-upload"
            className="p-2 rounded flex justify-center border-[1px] mb-4 mx-auto cursor-pointer text-center w-1/2"
          >
            Choose a video file
          </label>
        </div>

        <hr className="border-gray-300 w-full my-4" />

        <div className="my-10 w-3/4 flex-col justify-center mx-auto text-center">
          <p className="text-center mb-4 ">
            Provide the link of the video here 👇
          </p>
          <input
            type="text"
            placeholder="Give a link here"
            className="border border-gray-300 p-2 rounded mr-2 w-1/2"
          />
          <Link to="/player">
            <button className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition duration-200">
              Submit
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;
