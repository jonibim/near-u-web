import 'bootstrap/dist/css/bootstrap3.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import BootstrapVue from 'bootstrap-vue';
import PortalVue from 'portal-vue';
import AudioVisual from 'vue-audio-visual';
import VueRecord from '@codekraft-studio/vue-record';
import Vue from 'vue';
import App from './App.vue';
import router from './router';

Vue.use(PortalVue);

Vue.use(BootstrapVue);

Vue.use(VueRecord);

Vue.use(AudioVisual);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
