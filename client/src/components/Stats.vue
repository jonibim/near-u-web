<template>
  <b-card
  header="Stats"
  class="text-center">
    <div class='m-3'>
      <b-container class='bv-example-row'>
        <b-row>
          <b-col class='m-2 ' align-v="stretch" align-h="start">
            <ul style='list-style-type: none; text-align: left;'>
              <li>Status:
                <span v-show='active'
                style="color:green">
                  OK
                  </span>
                  <span v-show='!active'
                style="color:red">
                  Not connected
                  </span>
                </li>
              <li>Device: RPi A+</li>
              <li>Tasks: {{tasks}} </li>
              <li>Sensors: {{sensors}}</li>
            </ul>
          </b-col>
          <b-col class='m-2'>
            <b-img-lazy :src="image" fluid-grow>
            </b-img-lazy>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </b-card>
</template>

<script>
import axios from 'axios';
import { EventBus } from '../bus';

export default {
  name: 'Stats',
  data() {
    return {
      tasks: '',
      sensors: '',
      active: false,
      // eslint-disable-next-line
      image: require('../assets/img/rpi.png'),
    };
  },
  methods:
  {
    update() {
      EventBus.$on('gib-me-tasks', (data) => {
        this.tasks = data.length;
        console.log('tasks', this.tasks);
      });
      EventBus.$on('gib-me-sensors', (data) => {
        this.sensors = data.length;
      });
    },
    checkMe() {
      const path = 'https://10.42.0.115:5000/api/ping';
      axios
        .get(path)
        .then((res) => {
          if (res.data === 'pong!') {
            this.active = true;
          }
        })
        .catch((error) => {
          this.active = false;
          console.error(error);
        });
    },
  },
  created() {
    this.checkMe();
    this.update();
  },
};
</script>
