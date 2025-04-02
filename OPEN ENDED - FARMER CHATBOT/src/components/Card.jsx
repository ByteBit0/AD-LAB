import "../assets/styles.css";

const Card = ({ link, title, image, description }) => {
  return (
    <a href={link} className="card-link" target="_blank" rel="noopener noreferrer">
      <div className="card">
        <div className="upper">
          <h3 className="class1">{title}</h3>
        </div>
        <div className="lower">
          <img src={image} alt={title} className="cardimg" />
          <div className="overlay-text">{description}</div>
        </div>
      </div>
    </a>
  );
};

export default Card;
