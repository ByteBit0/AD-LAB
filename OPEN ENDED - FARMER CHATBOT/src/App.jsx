// export default App;
import "./assets/styles.css";
import Header from "./components/Header";
import Card from "./components/Card";
import Footer from "./components/Footer";

import img1 from "../public/images/spring-country-wide-summer-landscape.jpg";
// import img2 from "/images/2img.ng";

const App = () => {
  return (
    <div className="container">
      <Header />

      <div className="secondsection">
        <p className="second_section_p">
          🌾 <span style={{ color: "#2e7d32", fontWeight: "600" }}>
            Revolutionizing Agriculture
          </span>{" "}
          with <span style={{ color: "#00838f", fontWeight: "600" }}>Generative AI</span>
        </p>
      </div>

      <div className="thirdsection">
        <Card
          link="http://127.0.0.1:5000/"
          title="Kissan Copilot"
          image={img1}
          description="Interact with our smart AI to get real-time, insightful answers tailored to your farm's needs."
        />

        {/* <Card
          link="http://127.0.0.1:5000/weather"
          title="Agri Copilot WeatherGuard"
          image={img2}
          description="Stay ahead of unpredictable conditions with live weather insights for your crops."
        /> */}
      </div>

      <Footer />
    </div>
  );
};

export default App;
