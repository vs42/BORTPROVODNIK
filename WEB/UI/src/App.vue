<template>
    <div id="app">
        <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
        
        <b-navbar v-if="authenticated" toggleable="md" type="light" variant="light" class="navBar">

            <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

            <b-navbar-brand style="color: black; font-family: 'Roboto', sans-serif; font-size: 30px !important;">BORTPROVODNIK</b-navbar-brand>

            <b-collapse is-nav id="nav_collapse">

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">

                    <form style="display: flex !important; flex-direction:row-reverse !important; margin-right: 20px; margin-top: 5px !important;">
                        <input id="searchField" style="margin-left: 10px !important;" class="form-control form-control ml-3" type="text" placeholder="Поиск" aria-label="Search" v-on:change="updateSearch" v-on:keyup.enter="submitSearch" v-on:submit="submitSearch" >
                        <i style="margin-top: 10px !important; margin-right: 0px !important; margin-left: 5px !important;" class="fas fa-search" aria-hidden="true"></i>
                    </form>


                    <!-- <div v-if="onUploading" class="uploadProcessDiv">
                        <span class="uploadProcessSpan"> Идет загрузка:  </span>
                        <b-progress :value="filesUploaded" :max="filesToUpload" class="mb-3"></b-progress>
                    </div>

                    <div v-if="!onUploading" v-on:click="startUpload" class="iconDiv">
                        <div><img src="https://i.ibb.co/vJs3zrs/icon.png"  class="iconImg"/></div>
                        <span class="iconText">Загрузка</span>
                    </div>

                    <b-modal id="uploadModal" ref="uploadModal" hide-footer=true @hide="isModalShown=false" title="Загрузка фотографий">
                        <myUploader ref="myUploader" v-on:closeModal="isModalShown = false;" url="http://photoclo.ru/api/photos/"
                                    @upload-image-attempt="uploadAttempt();" @upload-image-finish="uploadFinish();"
                                    @upload-image-success='updateImagesOk();' @upload-image-failure='updateImagesFail();'
                                    @set-files-num="setFilesNum"  @start-upload="showProgress"> </myUploader>
                    </b-modal> -->

                    <div class="iconDiv" v-on:click="addTable" id="addDiv">
                        <img src="https://i.ibb.co/GCktzdq/baseline-note-add-black-48dp.png" id="addTableBtn"/>
                    </div>

                    <div class="iconDiv" v-on:click="logout" id="logoutDiv">
                        <div><img src="https://i.ibb.co/nLqCDNy/logout-512.png" class="iconImg"></div>
                        <span class="iconText"> Выйти</span>
                    </div>

                </b-navbar-nav>

            </b-collapse>
        </b-navbar>
        
        <div v-if="cnt == '0' && authenticated" class="greeting">
            <div style="margin-top: 70px !important"><img src="https://i.ibb.co/vZF4hfc/maxresdefault-2-removebg.png" alt="maxresdefault-2-removebg" border="0"></div>
            <span style="margin-top: 30px; font-size: 72px !important;" class="greetingText"> ЗДАРОВА УБЛЮДКИ</span>
        </div>
        <router-view @authenticated="setAuthenticated" ref="child" v-bind:cnt="cnt" @cntInc="cntInc()" @cntDec="cntDec()" @cntSet="cntSet"/>

    </div>
</template>

<script>
    import axios from 'axios';
    var modal = document.getElementById('id01');

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }


    export default {
        name: 'App',
        data() {
            return {
                authenticated: false,
                token: undefined,
                isModalShown: false,
                onUploading: false,
                filesUploaded: 0,
                filesToUpload: 0,
                isDiskSynchronized: false,
                // That's bullshit because of assync of JS:
                hasJustStarted: false,
                // That's bullshit because of assync of JS:
                cnt: 0,
                search: ''
            }
        },
        mounted() {
            var this_ = this;

            if (localStorage.hasOwnProperty('cnt')) {
                this.cnt = localStorage.cnt;
            }
            else {
                this.cnt = 0;
                localStorage.cnt = 0;
            }
            axios.get('/api/tokens/status',{ headers: {Authorization: "Token " + String(localStorage.token)}}).then(function (response) {
                if (!response.data.sync) {
                    this_.isDiskSynchronized = false;
                } else {
                    this_.isDiskSynchronized = true;
                }
            });
            if (localStorage.hasOwnProperty('token')) {
                this.token = localStorage.token;
                this.authenticated = true;
            }
            if(!this.authenticated) {
                this.$router.replace({ name: "login" });
            }
            else {
                this.$router.replace({name: "secure"});
            }
        },
        methods: {
            updateToken () {
                document.getElementsByClassName('myUploadBox')[0].__vue__.$props.my_header = {Authorization: "Token " + localStorage.token};
            },
            setAuthenticated(status) {
                this.authenticated = status;
            },
            logout() {
                var this_ = this;
                axios.post('/api/sign_out/', {Authorization: "Token " + String(localStorage.token)}).then(function () {
                    this_.authenticated = false;
                    this_.$router.replace({ name: "login" });
                    delete localStorage.token;
                });
            },
            updateImagesOk() {
                this.filesUploaded += 1;
                this.$refs.child.updateImages();
            },
            updateImagesFail() {
                this.$refs.child.updateImages();
            },
            resetUploader() {
                this.$refs.myUploader.resetUploader();
            },
            startUpload() {
                this.isModalShown=true;
                this.updateToken();
                this.resetUploader()
            },
            showProgress() {
                this.onUploading = true;
                this.hasJustStarted = true;
            },
            uploadAttempt() {
                this.onUploading = true;
            },
            uploadFinish() {
                if (this.hasJustStarted) {
                    this.hasJustStarted = false
                } else {
                    this.onUploading = false;
                    this.filesUploaded = 0;
                    this.filesToUpload = 0;
                }
            },
            setFilesNum(value) {
                this.onUploading = true;
                this.filesToUpload = value;
            },
            goToYandexDisk() {
                if (!this.isDiskSynchronized) {
                    axios.get('/api/tokens/code/',{ headers: {Authorization: "Token " + String(this.token)}}).then(function (response) {
                        window.location.href = response.data.url;
                    });
                }
            },
            cntInc() {
                this.cnt++;
                localStorage.cnt = this.cnt;
            },
            cntDec() {
                this.cnt--;
                localStorage.cnt = this.cnt;
            },
            cntSet(value) {
                this.cnt = Number(value);
                localStorage.cnt = this.cnt;
            },
            updateSearch(event) {
                this.search = event.target.value;
            },
            submitSearch() {
                this.$refs.child.search(this.search);
            },
            addTable() {
                this.cnt++;
                localStorage.cnt = this.cnt;
                console.log(this.$refs.child);
                this.$refs.child.addTable();
            }
        },
    }
</script>

<style>
    body {
        background-color: #EEEEEE !important;
    }
    h1 {
        padding: 0;
        margin-top: 0;
    }

    .active {
        background-color: #4CAF50;
        color: white;
    }

    button:hover {
        opacity: 0.8;
    }

    .dropAreaDragging{
        background-color: #ccc;
    }

    .navBar {
        border-bottom: 2px solid #3A78DE;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    
    #userImg {
        padding-bottom: 8px;
        height: 45px;
        width: auto;
    }

    .iconDiv {
        /*border: 1px solid grey;*/
        cursor: pointer;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: 5px;
        margin-right: 30px;
        display: flex;
        flex-direction: row;
        text-align: center;
    }

    #logoutDiv {
        margin-right: 10px !important;
    }

    .iconDiv:hover {
        background-color: rgba(58, 120, 222, 0.05) !important;
    }

    .iconText {
        font-weight: 100;
        font-family: 'Roboto', sans-serif;
        font-size: 17px;
        margin-left: 10px;
        margin-right: 10px;
    }

    .iconImg {
        width: 20px;
        height: 15px;
        margin-left: 0px;
    }

    .userImg {
        width: 20px;
        height: 20px;
        margin-left: 5px;
        margin-right: 3px;
    }

    #uploadModal {
        font-family: 'Roboto', sans-serif;
    }

    .uploadProcessDiv {
        margin-right: 30px;
        display: flex;
        flex-direction: column;
        text-align: center;
    }

    .uploadProcessSpan {
        margin-top: 5px;
    }

    #dropUser:hover .dropdown-menu{
        margin-top: 0;
        display: block;
    }

    .searchForm {
    }

    .searchField {
        width: 120vw !important;
        margin-right: 0px !important;
        margin-left: 30px !important;
    }

    .searchForm:hover,
    .searchForm:focus {
        background-color: rgba(0, 0, 0, 0) !important;
    }

    .greeting {
        display: flex;
        flex-direction: column;
        text-align: center;
    }

    .greetingImg {
        width: auto !important;
        max-width: 90vw;
        height: auto;
        max-height: 90vh;
    }

    .greetingText {
        font-weight: 100;
        font-family: 'Roboto', sans-serif;
        font-size: 19px;
    }

    #addDiv {
        height: 30px;
        width: auto;
    }

    #addTableBtn {
        height: 100%;
        width: auto;
    }

</style>