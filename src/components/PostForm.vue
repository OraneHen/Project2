<template>
    <div>
        <div class="form_title">New Post</div>
        <div class="form_div">
            <form @submit.prevent="post" id="post_form">
                <div class="input_div">
                    <label for="photo">Photo</label>
                    <input type="file" name="photo">
                </div>
                <div class="input_div">
                    <label for="caption">Caption</label>
                    <textarea class="caption" name="caption" id="" cols="10" rows="10"></textarea>
                </div>
                <div class="input_div new_post_button" id="input_div_button">
                    <button class="new_post_button" type="submit">Submit</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { default as router } from './../router';

let csrf_token = ref("");

async function getCsrfToken() {
    await fetch('/api/v1/csrf-token')
        .then(async (response) => await response.json())
        .then(async (data) => {
            csrf_token.value = data.csrf_token;
        })
        .catch(async error => console.log(await error))
}


async function post() {

    let post_form = document.getElementById('post_form');
    let form_data = new FormData(post_form);
    let username = localStorage.getItem('username');

    fetch('/api/v1/users/'+username+'/posts', {
        method: 'POST',
        body: form_data,
        headers: {
            Authorization: "Bearer " + localStorage.getItem('user-token'),
            'X-CSRFToken': csrf_token.value,
        },
    })
        .then(async function (response) {
             if (response.ok) {
                router.push('/')
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

onMounted(() => {
    getCsrfToken()
})



</script>

<style>
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

.caption{
    width:100% !important;
}

.new_post_button{
    width: 100% !important;
}

.input_div label {
    font-weight: bold;
}

.input_div textarea {
    width: 65%;
}

#input_div_button {
    display: flex;
    align-items: center;
    width: 50%;
    margin-left: auto;
    margin-right: auto;
    margin-top: 15px;
}

#input_div_button button {
    background-color: rgb(49, 224, 49);
    border: 1px solid rgb(49, 224, 49);
    border-radius: 5px;
    width: 100%;
    height: 10%;
    color: white;
    font-weight: bold;
}

#input_div_button button:hover {
    background-color: rgb(115, 255, 115);
    border: 1px solid rgb(115, 255, 115);
}

#input_div_button button:active {
    background-color: rgb(27, 155, 27);
    border: 1px solid rgb(27, 155, 27);
}
</style>