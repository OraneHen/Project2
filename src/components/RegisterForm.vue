<template>
    <div>
        <div class="form_title">Register</div>
        <div class="register_form_div">
            <form @submit.prevent="register" id="register_form">
                <div class="input_div_register">
                    <label for="username">Username</label>
                    <input type="text" name="username">
                </div>
                <div class="input_div_register">
                    <label for="password">Password</label>
                    <input type="text" name="password">
                </div>
                <div class="input_div_register">
                    <label for="firstname">Firstname</label>
                    <input type="text" name="firstname">
                </div>
                <div class="input_div_register">
                    <label for="lastname">Lastname</label>
                    <input type="text" name="lastname">
                </div>
                <div class="input_div_register">
                    <label for="email">Email</label>
                    <input type="text" name="email">
                </div>
                <div class="input_div_register">
                    <label for="location">Location</label>
                    <input type="text" name="location">
                </div>
                <div class="input_div_register">
                    <label for="biography">Biography</label>
                    <textarea name="biography" id="" cols="10" rows="10"></textarea>
                </div>
                <div class="input_div_register">
                    <label for="photo">Photo</label>
                    <input type="file" name="photo">
                </div>
                <div class="input_div_register" id="input_div_register_button">
                    <button type="submit">Register</button>
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


async function register() {

    let register_form = document.getElementById('register_form');
    let form_data = new FormData(register_form);

    fetch('/api/v1/register', {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    })
        .then(async function (response) {
            if (response.ok) {
                router.push('/base')
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
.register_form_div {
    border: 0.5px solid grey;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    padding: 15px 15px;
    width: 450px;
    box-shadow: 7px 7px 4px rgba(0, 0, 0, 0.25);
    background: white;
    align-items: center
}

.input_div_register {
    width: 370px;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    margin-bottom: 5px;
}

.input_div_register label {
    font-weight: bold;
}

.input_div_register textarea {
    width: 370px;
}

#input_div_register_button {
    display: flex;
    align-items: center;
    margin-left: auto;
    margin-right: auto;
    margin-top: 15px;
}

#input_div_register_button button {
    background-color: rgb(49, 224, 49);
    border: 1px solid rgb(49, 224, 49);
    border-radius: 5px;
    width: 100%;
    height: 35px;
    color: white;
    font-weight: bold;
}

#input_div_register_button button:hover {
    background-color: rgb(115, 255, 115);
    border: 1px solid rgb(115, 255, 115);
}

#input_div_register_button button:active {
    background-color: rgb(27, 155, 27);
    border: 1px solid rgb(27, 155, 27);
}
</style>