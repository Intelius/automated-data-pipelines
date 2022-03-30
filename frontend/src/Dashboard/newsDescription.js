import React from "react";
import placeholder from "../assets/placeholder-news.jpg";

const NewsDescription = (props) => {
  const handleNewsButton = (event) => {
    props.handleNewsButton();
  };

  if (props.articles) {
    return (
      <div className="news-container">
        <h3>News Over The Past 3 Days</h3>
        <div>
          {props.articles.map((article) => {
            return (
              <article
                key={article.news_sentiment_description.id}
                className="news"
              >
                <div className="news-img">
                  <img
                    src={
                      article.news_sentiment_description.image_url
                        ? article.news_sentiment_description.image_url
                        : placeholder
                    }
                    alt={"image related to the news"}
                  ></img>
                </div>
                <div className="news-description">
                  <div className="news-description__publisher">
                    <p>{article.news_sentiment_description.publisher}</p>
                    <p>
                      {article.news_sentiment_description.datetime.slice(0, 10)}
                      {"  "}
                      {article.news_sentiment_description.datetime.slice(
                        11,
                        16
                      )}
                    </p>
                  </div>
                  <div className="news-description__info">
                    <a href={article.news_sentiment_description.article_url}>
                      {article.news_sentiment_description.title}
                    </a>
                    <p className="news-description__info-p">
                      {article.news_sentiment_description.description}
                    </p>
                    <div className="news-description__sentiment">
                      <div className="news-description__sentiment-influence">
                        <p>Influence </p>
                        <div className="news-description__sentiment-influence-value">
                          <p>
                            {article.news_sentiment.compound_influence_score > 0
                              ? "+"
                              : ""}
                          </p>
                          <p>
                            {article.news_sentiment.compound_influence_score.toFixed(
                              3
                            )}
                          </p>
                        </div>
                      </div>
                      <div
                        className={
                          article.news_sentiment.sentiment_score === "Positive"
                            ? "news-description__sentiment-score news-description__sentiment-positive"
                            : article.news_sentiment.sentiment_score ===
                              "Negative"
                            ? "news-description__sentiment-score news-description__sentiment-negative"
                            : "news-description__sentiment-score"
                        }
                      >
                        <p>{article.news_sentiment.sentiment_score}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
        <div
          className={
            props.error && props.articles.length <= 0
              ? "news-message"
              : "news-message__disable"
          }
        >
          <p>Sorry, there are no news to show. Come back later! </p>
        </div>
        <div className="news-button">
          <button
            className={
              props.limit === 16
                ? "news-button__disable"
                : props.error
                ? "news-button__disable"
                : ""
            }
            onClick={handleNewsButton}
          >
            Show More
          </button>
        </div>
      </div>
    );
  } else {
    return (
      <div className="news-container">
        <h3>News Over The Past 3 Days</h3>

        <div className={"news-message"}>
          <p>Sorry, there are no news to show. Come back later! </p>
        </div>
      </div>
    );
  }
};

export default NewsDescription;
