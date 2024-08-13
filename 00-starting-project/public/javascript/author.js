const showAuthors = document.getElementById("show");
const listAuthors = document.getElementById("list-authors");
const hideAuthors = document.getElementById("hide");

function showAuthorsOnPage() {
  listAuthors.style.display = "block";
}

function hideAuthorsOnpage() {
  listAuthors.style.display = "none";
}

showAuthors.addEventListener("click", showAuthorsOnPage);
hideAuthors.addEventListener("click", hideAuthorsOnpage);
