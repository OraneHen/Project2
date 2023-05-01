<template>
    <div class="user_container">
        <div class="user_container_inner">
            <div class="user_profile">
                <div class="user_profile_image_container">
                    <img class="user_profile_image" :src=user.user_profile />
                </div>
                <div class="user_details">
                    <div class="user_name">{{ user.first_name + ' ' + user.last_name }}</div>
                    <div class="user_location">{{ user.location }}</div>
                    <div class="user_joined_on">{{ user.joined_on }}</div>
                    <div class="user_biography">{{ user.biography }}</div>
                </div>
                <div class="user_stats">
                    <div class="user_stats_inner">
                        <div class="stats">
                            <div class="stats_posts_container">
                                <div class="stats_count">{{user.posts}}</div>
                                <div class="stats_title">Posts</div>
                            </div>
                            <div class="stats_follows_container">
                                <div class="stats_count">{{user.follows}}</div>
                                <div class="stats_title">Following</div>
                            </div>
                        </div>
                        <div>
                            <div v-if="!user.is_current_user && !user.is_following" class="input_div follow_btn" id="follow_btn">
                                <button type="submit" @click="followUser">Follow</button>
                            </div>
                            <div v-if="!user.is_current_user && user.is_following" class="input_div" id="div_button">
                                <button type="submit">Following</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="user_posts_container">
            <div v-for="post in posts" class="user_post_img_container">
                <img class="user_post_img" :src=post.photo />
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from 'vue-router'
let posts = ref("");
let user = ref("");
let csrf_token = ref("");

const route = useRoute()

onMounted(() => {
    getUserPosts()
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

async function getUserPosts() {
    fetch('/api/v1/users/' + route.params.id + '/posts', {
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
            user.value = data.user;
        })
        .catch(async function (error) {
            console.log(await error)
        })
}

async function followUser() {
    fetch('/api/v1/users/' + route.params.id + '/follow', {
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
                getUserPosts();
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



</script>

<style>
.user_container_inner {
    display: flex;
    width: 100%;
    max-width: 930px;
    display: flex;
    flex-direction: row;
    padding: 0 5px;
}

.user_profile {
    display: flex;
    width: 100%;
    max-width: 930px;
    display: flex;
    flex-direction: row;
    padding: 5px;
    border: 1px solid #afafaf;
    border-radius: 4px;
    background: white;
}

.user_profile_image_container {
    display: flex;
    width: 150px;
    height: 150px;
    position: relative;
    overflow: hidden;
    margin: 5px 5px;
}

.user_profile_image {
    width: 150px;
    height: 150px;
    object-fit: cover;
    object-position: center center;
}

.user_container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.user_name{
    font-weight: 500;
    font-size: 18px;
    color: #555555;
    margin-bottom: 10px;
}

.user_location {
    font-size: 16px;
    color: #555555;
}

.user_biography {
    font-size: 16px;
    color: #555555;
}

.stats_count{
    font-size: 24px;
    color: #555555;
    font-weight: 500;
}

.stats_title{
    font-size: 18px;
    color: #a6a6a6;
    font-weight: 500;
}

.user_joined_on{
    font-size: 16px;
    color: #555555;
    margin-bottom: 5px;
}

.user_posts_container {
    width: 100%;
    max-width: 930px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}

.user_post_img_container {
    display: flex;
    width: 300px;
    height: 300px;
    position: relative;
    overflow: hidden;
    margin: 5px 5px;
}

.user_post_img {
    width: 300px;
    height: 300px;
    object-fit: cover;
    object-position: center center;
}


.user_details {
    flex-grow: 1
}

.user_stats {
    min-width: 150px;
    margin-right: 10px;
}

.user_stats_inner{
    padding-top: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
}

.stats{
    display: flex;
}

.stats_posts_container{
    min-width: 75px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.stats_follows_container{
    min-width: 75px;
    display: flex;
    flex-direction: column;
    align-items: center;
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

#follow_btn button {
    background-color: rgb(49, 224, 49);
    border: 1px solid rgb(49, 224, 49);
    border-radius: 5px;
    width: 100%;
    height: 10%;
    color: white;
    font-weight: bold;
}

#follow_btn button:hover {
    background-color: rgb(115, 255, 115);
    border: 1px solid rgb(115, 255, 115);
}

#follow_btn button:active {
    background-color: rgb(27, 155, 27);
    border: 1px solid rgb(27, 155, 27);
}
</style>