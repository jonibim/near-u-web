<template>
  <b-card
    overlay
    :img-src="image"
    img-alt="Card Image"
    text-variant="white"
    title="Troubleshooting"
  >
    <b-card-text>
      Is there any problem? Maybe we can help you!
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      errorMsg: '',
      // eslint-disable-next-line
      image: require('../assets/img/settings.jpg'),
    };
  },
};
</script>
