<template>
<div>
  <b-container class="">
    <b-row class=''>
      <b-col class='m-2'>
        <Login/>
      </b-col>
    </b-row>
    <b-row>
      <b-col class='m-2' align-self="stretch">
          <Notifications/>
      </b-col>
      <b-col class='m-2'>
          <Stats/>
      </b-col>
    </b-row>
    <b-row class="justify-content-center align-self-center">
      <b-col class = 'm-2'>
        <Messages/>
      </b-col>
    </b-row>
  </b-container>
  <br><br><br><br><br><br>
  <footer>
  <br>
  <p>Group-215 ED</p>
  <p>(Alpha) Prototype Version</p>
</footer>
</div>
</template>

<script>
// @ is an alias to /src
import Notifications from '@/components/Notifications.vue';
import Stats from '@/components/Stats.vue';
import Messages from '@/components/Messages.vue';
import Login from '@/components/Login.vue';

export default {
  name: 'Menu',
  components: {
    Messages,
    Stats,
    Notifications,
    Login,
  },
};
</script>

<style>
footer {
  text-align: center;
  padding: 5px;
  background-color: #d4feff;
  color:black;
}
</style>
