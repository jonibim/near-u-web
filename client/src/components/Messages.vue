<template>
  <b-card
  header="Messages"
  class="text-center">
    <div id='myContainer' class='m-2'>
      <b-alert show variant='dark' v-show='tasks.length === 0'>
        There are currently no registered messages
      </b-alert>
      <table class='table table-hover'>
        <thead></thead>
        <tbody>
          <tr
            v-for='(task, index) in tasks'
            :key='index'
            v-bind:class="[active === task.id ? 'table-success' : '']"
          >
            <td>
              {{ task.title }}
              <br />
              {{ task.configurations[0].addead_at }}
            </td>
            <td>
              <!-- <span v-if='book.read'>Yes</span>
                <span v-else>No</span> -->
            </td>
            <td>
              <button
                type='button'
                class='btn btn-primary'
                v-show='active !== task.id'
                @click='setActive(task)'
              >
                Set Active
              </button>

              <button
                type='button'
                class='btn btn-light'
                v-show='active === task.id'
                @click='setDeactive()'
              >
                Deactivate
              </button>
            </td>
            <td>
              <div class='btn-group' role='group'>
                <!-- <button type='button' class='btn btn-warning'>Update</button> -->
                <button
                  type='button'
                  class='btn btn-danger'
                  @click='onDeleteTask(task)'
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <b-button v-b-modal.modal-1> Add Message </b-button>
    </div>
    <b-modal
      ref='addRecordingModal'
      id='modal-1'
      size='lg'
      centered
      hide-footer
      title='Message Recorder'
    >
      <b-form @submit='onSubmit' @reset='onReset' class='w-100'>
        <b-container class='bv-example-row'>
          <b-row>
            <b-col class='m-2'>
              <b-form-group
                id='form-title-group'
                label='Title:'
                label-for='form-title-input'
              >
                <b-form-input
                  id='form-title-input'
                  type='text'
                  v-model='addRecording.title'
                  required
                  placeholder='Enter title'
                >
                </b-form-input>
              </b-form-group>
              <b-form-group
                id='form-sensor-group'
                label='Send to:'
                label-for='form-sensor-input'
              >
                <b-form-select
                  id='form-sensor-input'
                  type='text'
                  :options='all_sensors'
                  v-model='addRecording.sensor'
                  @change='onChange'
                  required
                  placeholder='Front door'
                >
                </b-form-select>
              </b-form-group>
              <b-form-group
                id='form-condition-group'
                label='Playback when:'
                label-for='form-condition-input'
              >
                <b-form-select
                  id='form-condition-input'
                  :options='all_conditions'
                  v-model='addRecording.condition'
                  required
                  placeholder='Front door is opened'
                >
                </b-form-select>
              </b-form-group>
              <b-form-group
                id='form-repeat-group'
                label='Repetitions: '
                label-for='form-repeat-input'
              >
                <b-alert show variant='info'> Set 0 for unlimited </b-alert>
                <b-form-spinbutton
                  id='form-repeat-input'
                  v-model='addRecording.repeat'
                  min='-1'
                  max='10'
                  size='sm'
                  label='Repetitions: '
                >
                </b-form-spinbutton>
              </b-form-group>
              <b-form-group id='form-notification-group'>
                <b-form-checkbox-group id='form-checks'>
                  <b-form-checkbox value='true'
                    >Receive notifiactions?</b-form-checkbox
                  >
                </b-form-checkbox-group>
              </b-form-group>
            </b-col>
            <b-col class='m-2 row justify-content-center align-self-center'>
              <b-container class='bv-recording-row'>
                <b-row class='justify-content-center'>
                  <b-alert show variant='info'
                    >Press the button below to start recording</b-alert
                  >
                </b-row>
                <b-row class='justify-content-center'>
                  <vue-record-audio
                    :mode='recMode'
                    @result='onResult'
                    @stream='onStream'
                  />
                  <div>
                    <audio ref='player'></audio>
                    <av-media
                      type='frequ'
                      :media='media'
                      line-color='darkorange'
                    />
                  </div>
                </b-row>
              </b-container>
              <b-container class='bv-playback-row'>
                <b-row
                  v-if='showMedia'
                  class='text-center justify-content-center'
                >
                  <av-waveform
                    :audio-src='audio'
                    :playtime-clickable='true'
                    :canv-width='300'
                  />
                </b-row>
              </b-container>
              <!-- <b-alert :show='mediaNotSupported' variant='danger'>
              You browser does not support AvMedia component. <br />
              No suitable media device found (navigator.mediaDevices is not
              defined)
            </b-alert>
            <b-button
              v-if='!mediaNotSupported && !showMedia'
              variant='outline-primary'
              @click='showMedia = true'
            >
              Start av-media
            </b-button>
            <AvMediaDemo v-if='showMedia' /> -->
            </b-col>
          </b-row>
        </b-container>
        <hr />
        <b-button-group class='float-right'>
          <b-button v-if='!audio' disbaled>Submit</b-button>
          <b-button v-if='audio' type='submit' variant='primary'
            >Submit</b-button
          >
          <b-button type='reset' variant='danger'>Reset</b-button>
        </b-button-group>
        <b-button variant='dark' @click='onClose'>Close</b-button>
      </b-form>
    </b-modal>
  </b-card>
</template>

<script>
import axios from 'axios';
import { EventBus } from '../bus';

export default {
  name: 'Messages',
  data() {
    return {
      addRecording: {
        title: null,
        sensor: null,
        condition: null,
        repeat: 0,
        notification: null,
      },
      showMedia: false,
      media: null,
      audio: null,
      recMode: 'press',
      tasks: [],
      data: null,
      all_sensors: [],
      all_conditions: [],
      datamedia: null,
      active: null,
      timer: null,
    };
  },
  methods: {
    converToList(data) {
      // console.log(data.sensors);
      // eslint-disable-next-line
      for (const key in data.sensors) {
        // eslint-disable-next-line
        if (data.sensors.hasOwnProperty(key)) {
          const json = {
            value: data.sensors[key].id,
            text: data.sensors[key].s_type,
          };
          this.all_sensors.push(json);
        }
      }
      // console.log('all_sensor', this.all_sensors);
    },
    getActive() {
      const path = 'https://10.42.0.115:5000/api/active/';
      axios
        .get(path)
        .then((res) => {
          this.converToList(res.data);
          this.data = res.data.sensors;
          console.log('data', this.data);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getSensors() {
      const path = 'https://10.42.0.115:5000/api/sensors/';
      axios
        .get(path)
        .then((res) => {
          this.converToList(res.data);
          this.data = res.data.sensors;
          // console.log('org_sensors', this.data);
          // this.sensors = this.data
          EventBus.$emit('gib-me-sensors', this.all_sensors);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getTasks() {
      const path = 'https://10.42.0.115:5000/api/tasks/';
      axios
        .get(path)
        .then((res) => {
          // console.log(res);
          // console.log('respond-data', res.data.tasks);
          if (this.tasks !== res.data.task) {
            this.tasks = res.data.tasks;
            // console.log('taskso', this.tasks);
          }
          EventBus.$emit('gib-me-tasks', this.tasks);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    postRecording(payload) {
      const path = 'https://10.42.0.115:5000/api/tasks/';
      axios
        .post(path, payload)
        .then(() => {
          this.getTasks();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    postActive(payload) {
      const path = 'https://10.42.0.115:5000/api/active/';
      axios
        .post(path, payload)
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    removeTask(taskID) {
      const path = `https://10.42.0.115:5000/api/tasks/${taskID}/`;
      axios
        .delete(path)
        .then(() => {
          this.getTasks();
          console.log('done');
        })
        .catch((error) => {
          console.log(error);
        });
    },
    onDeleteTask(task) {
      this.removeTask(task.id);
    },
    onChange() {
      this.all_conditions = [];
      // eslint-disable-next-line
      for (const key in this.data) {
        // eslint-disable-next-line
        if (this.data.hasOwnProperty(key)) {
          if (this.data[key].id === this.addRecording.sensor) {
            const tmpCondition = this.data[key].conditions;
            // eslint-disable-next-line
            for (const key in tmpCondition) {
              // console.log('key', key);
              // eslint-disable-next-line
              if (tmpCondition.hasOwnProperty(key)) {
                // console.log('all_conditions', this.tmpCondition);
                const json = {
                  value: tmpCondition[key].id,
                  text: tmpCondition[key].condition,
                };
                this.all_conditions.push(json);
              }
            }
            break;
          }
        }
      }
      // console.log('all_conditions', this.all_conditions);
    },
    onResult(data) {
      // console.log('The blob data:', blob);
      const blob = data.slice(0, data.size, 'audio/wav');
      const reader = new FileReader();
      reader.readAsDataURL(blob);
      reader.onloadend = () => {
        const base64data = reader.result.split(',')[1];
        this.datamedia = base64data;
      };
      this.audio = window.URL.createObjectURL(data);
      // console.log(this.audio);
      this.showMedia = true;
    },
    onStream(data) {
      this.showMedia = false;
      // console.log(data);
      this.media = data;
    },
    initForm() {
      this.addRecording.title = '';
      this.addRecording.sensor = '';
      this.addRecording.condition = '';
      this.notification = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addRecordingModal.hide();
      const payload = {
        title: this.addRecording.title,
        s_type: this.addRecording.sensor,
        condition: this.addRecording.condition,
        configuration: {
          notifications: false,
          message: this.datamedia,
          repeat: 0,
        },
      };
      this.postRecording(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.showMedia = false;
      this.audio = null;
      this.getTasks();
      this.initForm();
    },
    onClose() {
      this.initForm();
      this.$refs.addRecordingModal.hide();
    },
    setActive(task) {
      this.postActive(task);
      this.active = task.id;
    },
    setDeactive() {
      const path = 'https://10.42.0.115:5000/api/deactive/';
      axios
        .get(path)
        .then((res) => {
          const t = res.data;
          console.log(t);
          this.active = null;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    this.getSensors();
    if (!navigator.mediaDevices) {
      this.mediaNotSupported = true;
    }
  },
  created() {
    this.getTasks();
    this.timer = setInterval(this.getTasks, 500000);
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
};
</script>

<style>
body.modal-open #app{
    -webkit-filter: blur(1px);
    -moz-filter: blur(1px);
    -o-filter: blur(1px);
    -ms-filter: blur(1px);
    filter: blur(10px);
}
</style>
