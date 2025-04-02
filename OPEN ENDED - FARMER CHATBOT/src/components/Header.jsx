import "../assets/styles.css";
import logo from "/images/4img.png";

const Header = () => {
  return (
    <div className="firstsection">
      <div className="leftmost">
        <img src={logo} alt="Kissan-AI" className="iconimg" />
      </div>
      <div className="rightmost">
        <h1 className="ubuntu-medium">KissanAi</h1>
      </div>
    </div>
  );
};

export default Header;
