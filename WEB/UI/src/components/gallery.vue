<template>
    <div class="gallery">

        <div v-for="(tabless, index1) in tableRows" style="display: flex; flex-direction: row; flex-wrap: nowrap; width: 100%; height: auto">
            <div class="myContainer" v-for="(table, index2) in tabless" v-on:click='clicked(index1, index2)' v-bind:key="table.name">
                <img class="imageItem" v-bind:src="table.image" v-bind:style="styles[index1][index2]" alt=""/>
                <span class="nameView">{{table.name}}</span>
            </div>
        </div>

        <div id="myModal" class="imageModal">
            <span class="buttonCarousel" id="closeImageButton">&times;</span>
            <!-- <div class="bottomButtons">
                <span id="deleteImageButton">Удалить</span>
                <span id="downloadImageButton">Загрузить</span>
            </div> -->
            <div class='innerContent'>
                <div class="carouselButton" id="prevButton" v-on:click="prev()">
                    <span>&#8249;</span>
                </div>
                <div id="overIBS">
                    <div class="image-modal-content">
                        <!-- <tableItem ref="child" id="tableBigShow" v-bind:table="tables[index]"/> -->
                    </div>
                </div>
                <div class="carouselButton" id="nextButton" v-on:click="next()">
                    <span>&#8250;</span>
                </div>
            </div>
        </div>

 
    </div>
</template>

<script>
    import imageItem from './imageItem.vue';
    import tableItem from './tableItem.vue';
    import axios from 'axios';

    export default {
        name: 'gallery',
        components: {
            imageItem,
            tableItem,
        },
        props: {
            tables: {
              type: Array,
              default () {
                  return [];
              }
            },
        },
        data() {
            return {
                index: null,
                tableNow: [],
                recompute: 0,
                lastTime: 0,
            };
        },
        watch: {
            index(value) {
                this.tablesNow = [];
                this.tableNow = this.tables[value];
            },
        },
        created: function () {
            document.onkeydown = this.onkeydown;
            window.addEventListener('resize', this.updateStyles);
            this.updateStyles();
        },
        mounted: function () {
            this.updateStyles();
        },
        destroyed() {
            window.removeEventListener('resize', this.updateStyles);
        },
        computed: {
            styles: function() {
                var margin = 2;
                this.tables;
                this.recompute;
                var st = [];
                var w = window.innerWidth - 10;
                for (var i = 0; i < this.tables.length; ++i) {
                    var sz = st.length;
                    st.push([]);
                    var j = i;
                    var sum = 0;
                    while (j < this.tables.length && (j == i || sum + Math.ceil(this.tables[j].width * 200 / this.tables[j].height) + margin <= w)) {
                        sum += Math.ceil(this.tables[j].width * 200 / this.tables[j].height) + margin;
                        ++j;
                    }
                    var h1 = Math.floor(199 * (w - (j - i) * margin) / (sum - (j - i) * margin));
                    if (j == this.tables.length) {
                        if (h1 < 250) {
                            for (var k = i; k < j; ++k) {
                                st[sz].push('height: ' + h1 + 'px !important;');
                            }
                        }
                        else {
                            for (var k = i; k < j - 1; ++k) {
                                st[sz].push('height: ' + 200 + 'px !important;');
                            }
                            st[sz].push('height: 200px !important; margin-right: auto !important; margin-left: 5px;');
                        }
                    }
                    else {
                        var sum2 = sum;
                        sum2 += Math.ceil(this.tables[j].width * 200 / this.tables[j].height) + margin;
                        var h2 = Math.floor(199 * (w - (j - i + 1) * margin) / (sum2 - (j - i + 1) * margin));
                        if (Math.abs(h2 / 200 - 1) < Math.abs(h1 / 200 - 1)) {
                            for (var k = i; k <= j; ++k) {
                                st[sz].push('height: ' + h2 + 'px !important;');
                            }
                            ++j;
                        }
                        else {
                            for (var k = i; k < j; ++k) {
                                st[sz].push('height: ' + h1 + 'px !important;');
                            }
                        }
                    }
                    i = j - 1;
                }
                console.log('st = ', st);
                return st;
            },
            tableRows: function () {
                console.log('tables = ', this.tables);
                var margin = 2;
                this.tables;
                this.recompute;
                var ir = [];
                var w = window.innerWidth - 10;
                for (var i = 0; i < this.tables.length; ++i) {
                    var sz = ir.length;
                    ir.push([]);
                    var j = i;
                    var sum = 0;
                    while (j < this.tables.length && (j == i || sum + Math.ceil(this.tables[j].width * 200 / this.tables[j].height) + margin <= w)) {
                        sum += Math.ceil(this.tables[j].width * 200 / this.tables[j].height) + margin;
                        ++j;
                    }
                    var h1 = Math.floor(199 * (w - (j - i) * margin) / (sum - (j - i) * margin));
                    if (j == this.tables.length) {
                        if (h1 < 250) {
                            for (var k = i; k < j; ++k) {
                                ir[sz].push(this.tables[k]);
                            }
                        }
                        else {
                            for (var k = i; k < j - 1; ++k) {
                                ir[sz].push(this.tables[k]);
                            }
                            ir[sz].push(this.tables[j - 1]);
                        }
                    }
                    else {
                        var sum2 = sum;
                        sum2 += Math.ceil(this.tables[j].width * 200 / this.tables[j].height) + margin;
                        var h2 = Math.floor(199 * (w - (j - i + 1) * margin) / (sum2 - (j - i + 1) * margin));
                        if (Math.abs(h2 / 200 - 1) < Math.abs(h1 / 200 - 1)) {
                            for (var k = i; k <= j; ++k) {
                                ir[sz].push(this.tables[k]);
                            }
                            ++j;
                        }
                        else {
                            for (var k = i; k < j; ++k) {
                                ir[sz].push(this.tables[k]);
                            }
                        }
                    }
                    i = j - 1;
                }
                console.log('ir = ', ir);
                return ir;
            }
        },
        mounted: function () {
            var modal = document.getElementById('myModal');

            var span = document.getElementById('closeImageButton'); 
            span.onclick = function () {
                this.index = null;
                modal.style.display = "none";
            }

            // var span2 = document.getElementById('deleteImageButton');
            // var span3 = document.getElementById('downloadImageButton');
            // var this_ = this;
            // span2.onclick = function () {
            //     if (this_.index == null) {
            //         return;
            //     }
            //     this_.$emit('cntDec');
            //     var id_ = this_.images[this_.index].id;
            //     this_.images.splice(this_.index, 1);
            //     this_.imagesBig.splice(this_.index, 1);
            //     if (this_.index == this_.images.length) {
            //         this_.index = 0;
            //     }
            //     this_.deleteLastFaces();
            //     if (this_.images.length == 0) {
            //         this_.close();
            //     }
            //     axios.delete('http://photoclo.ru/api/photos/' + id_ + '/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
            //     }).catch(function (error) {
            //         console.log(error);
            //     });
            // };

            // span3.onclick = function () {
            //     axios.get('http://photoclo.ru/api/photos/' + this_.images[this_.index].id + '/download/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
            //         var url = response.data.url;
            //         if (response.data.type == "Yandex") {
            //             download2(response.data.url);
            //         }
            //         else {
            //             download(url);
            //         }
            //     }).catch(function (error) {
            //         console.log(error);
            //     });
            // }
        },
        methods: {
            clicked(index1, index2) {
                var id = index2;
                for (var j = 0; j < index1; ++j) {
                    id += this.tableRows[j].length;
                }
                this.index = id;
                var modal = document.getElementById('myModal');
                modal.style.display = "flex";
            },
            updateStyles() {
                this.recompute += 1;
                this.lastTime = (new Date()).getTime();
            },
            next() {
                this.deleteLastFaces()
                this.index += 1;
                if (this.index == this.tables.length) {
                    this.index = 0;
                }
            },
            prev() {
                this.deleteLastFaces()
                this.index -= 1;
                if (this.index < 0) {
                    this.index = this.tables.length - 1;
                }
            },
            close() {
                this.deleteLastFaces();
                this.index = null;
                document.getElementById('myModal').style.display = "none";
            },
            onkeydown(e) {
                if (e.key == "Escape") {
                    this.close();
                }
                else if (e.key == "ArrowRight") {
                   this.next();
                }
                else if (e.key == "ArrowLeft"){
                    this.prev();
                }
            }
        }
    }
</script>

<style>
    .gallery {
        display: flex;
        flex-direction: column;
        margin: 5px;
    }

    .imageModal {
        display: none; 
        position: fixed;
        z-index: 1; 
        padding-top: 0px;
        left: 0;
        top: 0;
        justify-content: space-around;
        width: 100%; 
        height: 100%; 
        overflow: auto;
        background-color: rgb(0,0,0);
        background-color: rgba(0,0,0,0.9);
    }

    .image-modal-content {
        display: flex;
        justify-content: space-around;
        alignment-baseline: central;
        width: 100%;
        height: auto;
        max-height: 
    }
    
    .image-modal-content { 
        animation-name: zoom;
        animation-duration: 0.6s;
    }

    @keyframes zoom {
        from {transform:scale(0)} 
        to {transform:scale(1)}
    }

    .close {
        outline: none !important;
        border: 0px !important;
    }

    .buttonCarousel {
        position: absolute;
        color: #999 !important; 
        font-size: 31px;
        font-family: 'Roboto', sans-serif;
        transition: 0.3s;
    }

    #closeImageButton {
        position: absolute;
        top: 10px;
        right: 20px;
    }

    #deleteImageButton,
    #downloadImageButton {
        color: #AAA !important;
        font-size: 15px;
        font-family: 'Roboto', sans-serif;
        margin: 5px;
    }

    #deleteImageButton:hover,
    #deleteImageButton:focus,
    #downloadImageButton:hover, 
    #downloadImageButton:focus {
        color: #FFF !important;
        cursor: pointer;
    }

    .bottomButtons {
        position: absolute;
        transition: 0.3s;
        bottom: 5px;
        width: auto;
    }

    .buttonCarousel:hover,
    .buttonCarousel:focus {
        color: #FFF !important;
        text-decoration: none;
        cursor: pointer;
    }

    .carouselButton {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        overflow: visible;
        text-align: center;
        width: 100% !important;
        font-size: 40px;
        font-family: 'Roboto', sans-serif;
        color: #CCC !important;
        background-color: rgba(0, 0, 0, 0) !important;
        height: 100% !important;
        font-weight: bold;
        transition: 0.3s;
    }

    .carouselButton:hover,
    .carouselButton:focus {
        color: #FFF !important;
        text-decoration: none;
        cursor: pointer;
    }

    #prevButton span {
        position: absolute;
        left: 10px;
    }

    #nextButton span {
        position: absolute;
        right: 10px;
    }

    .innerContent {
        width: 100%;
        height: 100%;
        max-height: 100vh !important;
        overflow: hidden;
        display: flex;
        text-align: center;
    }

    #overIBS {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: auto;
        height: 100%;
        max-height: 100vh !important;
    }

    #myModal {
        max-height: 100vh !important;
    }

    .myContainer:hover {
        opacity: 0.8;
        cursor: pointer;
        width: auto;
    }

    .nameView {
        width: auto;
        background-color: rgba(0, 0, 0, 0);
        text-align: center;
        height: auto;
        font-family: 'Roboto', sans-serif;
        font-size: 15px;
    }

    .myContainer {
        display: flex;
        flex-direction: column;
        border: 0px solid black;
        margin: 1px;
        margin-top: 2px;
        margin-bottom: 2px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    .imageItem {
        width: auto;
    }
</style>