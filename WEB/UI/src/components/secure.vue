<template>
    <gallery v-bind:tables="tables" v-bind:cnt="cnt" @cntDec="cntDec()"/>
</template>

<script>

    import gallery from './gallery.vue';
    import axios from 'axios';
    
    import imageItem from './imageItem.vue'; 

    export default {
        components: {
            gallery,
            imageItem
        },
        name: 'Secure',
        props: ['cnt'],
        data() {
            return {
                tables: [],
                index: null,
            }
        },
        mounted() {
            var this_ = this;
            /*axios.get('GET_TABLES', { headers: {Authorization: "Token " + localStorage.token} }).then(function (response) {
                for (var i = 0; i < response.data.tables.length; ++i) {
                    this_.tables.push(response.data.tables[i]);
                }
                this_.$emit('cntSet', response.data.tables.length);
            }).catch(function (error) {
                console.log(error);
            });*/
            this.$emit('cntSet', 0);
        },
        methods: {
            addTable() {
                this.tables.push({image: 'https://i.ibb.co/zF1tqKT/maxresdefault-2.jpg', name: 'MORGENSHTERN', width: 180, height: 180, table: [[1], [2]]});
            },
            updateTables() {
                var this_ = this;
                /*axios.get('GET_TABLES', { headers: {Authorization: "Token " + localStorage.token} }).then(function (response) {
                    this_.tables = [];
                    for (var i = 0; i < response.data.tables.length; ++i) {
                        this_.tables.push(response.data.tables[i]);
                    }
                    this_.$emit('cntSet', response.data.tables.length);
                }).catch(function (error) {
                    console.log(error);
                });*/
            },
            cntDec() {
                this.$emit('cntDec');
            },
            // search(value) {
            //     if (value == '') {
            //         this.updateTables();
            //         return;
            //     }
            //     var this_ = this;
            //     axios.get('http://photoclo.ru/api/filter/', { headers: {Authorization: "Token " + localStorage.token}, params: {size: "m", query: value}}).then(function (response) {
            //         this_.images = [];
            //         for (var i = 0; i < response.data.photos.length; ++i) {
            //             this_.images.push(response.data.photos[i]);
            //         }
            //         this_.$emit('cntSet', response.data.photos.length);
            //     }).catch(function (error) {
            //         console.log(error);
            //     });
            //     axios.get('http://photoclo.ru/api/filter/', { headers: {Authorization: "Token " + localStorage.token}, params: {size: "o", query: value}}).then(function (response) {
            //         this_.imagesBig = [];
            //         for (var i = 0; i < response.data.photos.length; ++i) {
            //             this_.imagesBig.push(response.data.photos[i]);
            //         }
            //     }).catch(function (error) {
            //         console.log(error);
            //     });
            //     axios.get('http://photoclo.ru/api/avatars/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
            //         this_.avatars = [];
            //         for (var i = 0; i < response.data.avatars.length; ++i) {
            //             this_.avatars.push(response.data.avatars[i]);
            //         }
            //     }).catch(function (error) {
            //         console.log(error);
            //     });
            // }
        }
    }
</script>

<style scoped>
</style>
