<template>
    <div id="myContainer">
        <img id="imageItem" v-bind:src="imageURL" alt=""/>
        <span id="nameView">{{name}}</span>
    </div>
</template>

<script>
    import AutoRotate from './AutoRotate';
    import Vue from 'vue';
    Vue.component('autoRotate', AutoRotate);
	export default {
		name: 'imageItem',
		props: ['imageURL', 'name'],
		methods: {},
	}
</script>

<style scoped>
    #myContainer:hover {
    	opacity: 0.8;
    	cursor: pointer;
    }

    #nameView {
        background-color: rgba(0, 0, 0, 0);
        text-align: center;
        height: auto;
        font-family: 'Roboto', sans-serif;
        font-size: 15px;
    }

    #myContainer {
        display: flex;
        flex-direction: column;
        border: 0px solid black;
        margin: 1px;
        margin-top: 2px;
        margin-bottom: 2px;
        height: auto;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }
</style>