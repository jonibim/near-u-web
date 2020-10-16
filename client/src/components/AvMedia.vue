<template>
  <div>
    <audio ref="player"></audio>
    <av-media type="frequ" :media="media" line-color="darkorange" />
  </div>
</template>

<script>
export default {
  name: 'av-media-demo',
  data() {
    return {
      mtype: null,
      media: null,
    };
  },
  mounted() {
    const audio = this.$refs.player;
    const constraints = {
      audio: true,
      video: false,
    };
    navigator.mediaDevices.getUserMedia(constraints).then((media) => {
      this.media = media;
      audio.srcObject = media;
    });
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
