<template>
<div>
  <b-card
    overlay
    img-src="https://picsum.photos/900/250/?image=3"
    img-alt="Card Image"
    text-variant="white"
    title="Hello, X"
    style='text-align:left'
  >
    <b-card-text>
      <a id='button-like' @click='openModal()' class="stretched-link">Check your settings</a>
    </b-card-text>
  </b-card>
  <b-modal id="modal-center" ref='checkSettings' centered title="Settings"
  footer-bg-variant='light'>
      <b-tabs pills card vertical>
      <b-tab title="Account" active><b-card-text>
        In here you would be able to change user accounts and password
        </b-card-text></b-tab>
      <b-tab title="Device"><b-card-text>
        In here you would be able to configure upadate routines
        </b-card-text></b-tab>
      <b-tab title="Advanced"><b-card-text>
        In here you would be able to reset the device to default settings
      </b-card-text></b-tab>
    </b-tabs>
  </b-modal>
</div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      errorMsg: '',
    };
  },
  methods: {
    openModal() {
      this.$refs.checkSettings.show();
    },
  },
};
</script>

<style>
#button-like {
  color: wheat;
}
</style>
