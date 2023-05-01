<script setup>
import { ref, onMounted } from "vue";
import { default as router } from './../router';

let posts = ref("");
let csrf_token = ref("");

onMounted(() => {
  getPosts()
  getCsrfToken()
})

async function getCsrfToken() {
  await fetch('/api/v1/csrf-token')
    .then(async (response) => await response.json())
    .then(async (data) => {
      csrf_token.value = data.csrf_token;
    })
    .catch(async error => console.log(await error))
}

async function getPosts() {
  fetch('/api/v1/posts', {
    method: "GET",
    headers: {
    Accept: "application/json",
    Authorization: "Bearer " + localStorage.getItem('user-token'),
    "Content-Type": "application/json",
    }
  })
  .then(async function (response) {
      if (response.ok) {
        return response.json()
      }
      else if (response.status == 401) {
        localStorage.removeItem('user-token')
        window.location.reload()
      }
    }).then((data) => {
      posts.value = data.posts;
      console.log(posts.value)
    })
    .catch(async function (error) {
      console.log(await error)
    })
}

async function likePost(post_id) {
  fetch('/api/v1/posts/'+post_id+'/like', {
    method: "POST",
    headers: {
      Accept: "application/json",
      Authorization: "Bearer " + localStorage.getItem('user-token'),
      "Content-Type": "application/json",
      'X-CSRFToken': csrf_token.value,
    }
  })
    .then(async function (response) {
      if (response.ok) {
        getPosts();
      }
      else if (response.status == 401) {
        localStorage.removeItem('user-token')
        window.location.reload()
      }
    })
    .catch(async function (error) {
      console.log(await error)
    })
}

function newPost() {
  router.push('/post')
}

function userPosts(user_id) {
  router.push('/user/'+user_id)
}

</script>

<template>
  <div class="container">
    <div class="posts_container">
        <div v-for="post in posts" class="post">
          <div class="post_title" @click="userPosts(post.user_id)">
            <div class="user_img_container">
               <img :src="post.user_profile" class="user_img"/>
            </div>
            <div class="username">{{post.username}}</div>
          </div>
          <div class="post_img"> 
            <img :src="post.photo" class="img"/>
          </div>
          <div class="post_description">{{ post.caption }}</div>
          <div class="post_footer">
            <span class="like_container" @click="likePost(post.id)"><i class="icons icon_style fa fa-heart-o"></i><div class="post_likes">{{ post.likes }} Likes</div></span>
            <div class="post_date">{{post.created_on}}</div>
          </div>
        </div>
    </div>
    <div class="text-center post_nav">
      <div class="input_div" id="div_button">
          <button type="submit" @click="newPost">New Post</button>
      </div>
    </div>
  </div>
</template>

<style>
.container{
    display: flex;
    flex-direction: row;
    justify-content: center;
    margin: auto;
}

.post_title{
  display: flex;
  padding: 3px 5px;
}

.post_title:hover{
  cursor: pointer;
}

.posts_container{
    display: flex;
    flex-direction: column;
    max-width: 450px;
    width: 100%;
    margin-right: 50px;
}

.post{
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 450px;
    border: 1px solid #afafaf;
    border-radius: 4px;
    margin-bottom: 30px;
    background-color: white;
}

.post_img{
    display: flex;
    width: 450px;
    height: 250px;
    min-width: 200px;
    position: relative;
    overflow: hidden;
}

.post_footer{
  display: flex;
  justify-content: space-between;
  padding: 5px;
  color: #555555;
}

.post_description{
  padding: 5px;
  width: 100%;
  min-height: 125px;
  color: #555555;

}

.like_container{
    display: flex;
    flex-direction: row;
    align-content: flex-start;
    align-items: center;
}

.icon_style{
  font-size: 13px !important ;
  margin-right: 3px;
  margin-left: 3px;
}

.like_container:hover{
  cursor: pointer;
}

.img {
    width: 450px;
    height: 250px;
    object-fit: cover;
    object-position: center center; 
}

.user_img_container{
    display: flex;
    width: 25px;
    height: 25px;
    position: relative;
    overflow: hidden;
    margin: 5px 0;
}

.user_img {
    width: 25px;
    height: 25px;
    border-radius: 50%;
    object-fit: cover;
    object-position: center center; 
}

.username{
  margin: 5px 10px;
  font-weight: 500;
  color: #555555;
}

.form_div {
    border: 0.5px solid grey;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    padding: 15px 15px;
    width: 55%;
    box-shadow: 7px 7px 4px rgba(0, 0, 0, 0.25);
}

.input_div {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    margin-bottom: 5px;
}

.input_div label {
    font-weight: bold;
}

.input_div textarea {
    width: 65%;
}

.post_nav{
    min-width: 200px;
}

#div_button {
    display: flex;
    align-items: center;
}

#div_button button {
    background-color: rgb(49, 224, 49);
    border: 1px solid rgb(49, 224, 49);
    border-radius: 5px;
    width: 100%;
    height: 10%;
    color: white;
    font-weight: bold;
}

#div_button button:hover {
    background-color: rgb(115, 255, 115);
    border: 1px solid rgb(115, 255, 115);
}

#div_button button:active {
    background-color: rgb(27, 155, 27);
    border: 1px solid rgb(27, 155, 27);
}
</style>