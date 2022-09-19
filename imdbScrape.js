function getLoadedReviewsCount() {
  return document.querySelectorAll(".ipl-ratings-bar").length;
}

let failedAttempts = -1;
let lastReviewsCount = getLoadedReviewsCount();
await new Promise((resolve) => {
  let loadMoreInterval;
  loadMoreInterval = setInterval(() => {
    const newReviewsCount = getLoadedReviewsCount();
    if (newReviewsCount == lastReviewsCount) {
      failedAttempts += 1;
      console.log(`failure #${failedAttempts}...`);
    }
    if (failedAttempts > 5) {
      console.log(
        `ceasing to load more reviews with ${newReviewsCount} available`
      );
      clearTimeout(loadMoreInterval);
      resolve();
    }
    lastReviewsCount = newReviewsCount;
    document.querySelector("#load-more-trigger").click();
  }, 1000);
});

const containers = document.querySelectorAll(".review-container");

const data = Array.from(containers).map((c) => ({
  ratingText: c.querySelector(".ipl-ratings-bar")?.innerText?.trim(),
  rating: c.querySelector(".ipl-ratings-bar")
    ? parseInt(c.querySelector(".ipl-ratings-bar").innerText.split("/")[0])
    : -1,
  userURL: c.querySelector(".display-name-link a").href,
  userID: c.querySelector(".display-name-link a").href.match(/ur[0-9]+/)[0],
  userName: c.querySelector(".display-name-link").innerText.trim(),
  date: c.querySelector(".review-date").innerText.trim(),
  title: c.querySelector(".title").innerText.trim(),
}));
const dataString = JSON.stringify(data);
let link = document.createElement("a");
link.setAttribute(
  "href",
  "data:text/plain;charset=UTF-8," + encodeURIComponent(dataString)
);
link.download = "movie.json";
link.click();
