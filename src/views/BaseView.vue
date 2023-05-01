<template>
    <div class="base_container">
        <div>
            <RouterLink to="/Register" class="nav-link active"><button type="submit">Register</button></RouterLink>
            <RouterLink to="/Login" class="nav-link active"><button type="submit">Login</button></RouterLink>
        </div>
    </div>
</template>
  
<script setup>
import { RouterLink } from "vue-router";
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
  