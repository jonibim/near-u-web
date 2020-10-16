<template>
  <div class="home">
    <b-spinner v-show="!load" type="grow" label="Loading..."></b-spinner>
    <div v-show="load">
    <Menu/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Menu from '@/components/Menu.vue';

export default {
  name: 'Home',
  data() {
    return {
      load: false,
    };
  },
  methods: {
    reveal() {
      this.load = true;
    },
  },
  components: {
    Menu,
  },
  created() {
    setTimeout(this.reveal, 1000);
  },
};
</script>
