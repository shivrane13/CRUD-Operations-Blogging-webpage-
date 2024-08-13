const express = require("express");
const db = require("../data/database");

const router = express.Router();

router.get("/", function (req, res) {
  res.redirect("/posts");
});

router.get("/posts", async function (req, res) {
  const query = `
      SELECT posts.*,authours.name AS authours_name FROM posts 
      INNER JOIN authours ON posts.author_id = authours.id
  `;
  const [posts] = await db.query(query);
  res.render("posts-list", { posts: posts });
});

router.get("/new-post", async function (req, res) {
  const [authors] = await db.query("SELECT * FROM authours");
  res.render("create-post", { authors: authors });
});

router.post("/posts", async function (req, res) {
  const data = [
    req.body.title,
    req.body.summary,
    req.body.content,
    req.body.author,
  ];
  await db.query(
    "INSERT INTO posts(title, summary, body, author_id) VALUES(?)",
    [data]
  );
  res.redirect("/posts");
});

router.get("/posts/:id", async function (req, res) {
  const query = `
    SELECT posts.*, authours.name AS author_name, authours.email FROM posts 
    INNER JOIN authours on posts.author_id = authours.id
    WHERE posts.id= ?

  `;
  const [details] = await db.query(query, [req.params.id]);

  if (!details || details === 0) {
    return res.status(404).render("404");
  }

  const postData = {
    ...details[0],
    date: details[0].date.toISOString(),
    humanReadableDate: details[0].date.toLocaleDateString("en-IN", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    }),
  };

  res.render("post-detail", { details: postData });
});

router.get("/posts/:id/edit", async function (req, res) {
  const query = `
    SELECT * FROM posts WHERE ID = ?
  `;
  const [posts] = await db.query(query, [req.params.id]);

  if (!posts || posts === 0) {
    return res.status(404).render("404");
  }

  res.render("update-post", { post: posts[0] });
});

router.post("/posts/:id/edit", async function (req, res) {
  const query = `
    UPDATE posts SET title=? , summary = ?, body = ?
    WHERE id = ?
  `;

  await db.query(query, [
    req.body.title,
    req.body.summary,
    req.body.content,
    req.params.id,
  ]);

  res.redirect("/posts");
});

router.post("/posts/:id/delete", async function (req, res) {
  await db.query("DELETE FROM posts WHERE id = ?", [req.params.id]);
  res.redirect("/posts");
});

router.get("/login", async function (req, res) {
  const [authors] = await db.query("SELECT * from authours");
  const data = await db.query("SELECT count(id) AS acount FROM authours");
  const acount = data[0][0].acount.toLocaleString();
  res.render("author", { acount: acount, authors: authors });
});

router.post("/login", async function (req, res) {
  const data = [req.body.aname, req.body.email];
  await db.query("INSERT INTO authours(name, email) VALUES (?)", [data]);
  res.redirect("/login");
});

router.post("/login/:id/delete", async function (req, res) {
  await db.query("DELETE FROM authours WHERE id = ?", [req.params.id]);
  res.redirect("/login");
});

module.exports = router;
