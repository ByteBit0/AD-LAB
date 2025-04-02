import "../assets/styles.css";
import copyrightIcon from "/images/5img.png";

const Footer = () => {
  return (
    <footer className="fourthsection">
      <div className="left">
        <a className="ubuntu-medium" href="http://127.0.0.1:5000/">
          Chat
        </a>
        {/* <a className="ubuntu-medium" href="http://127.0.0.1:5000/weather">
          Weather
        </a> */}
        {/* <a className="ubuntu-medium" href="https://kissan.ai/about">
          About
        </a> */}
      </div>
      <div className="right">
        {/* <img
          className="footer-icon"
          src={copyrightIcon}
          alt="copyright symbol"
        /> */}
        <span className="ubuntu-medium footer-text">
          © KissanAI, 2025. All rights reserved.
        </span>
      </div>
    </footer>
  );
};

export default Footer;
