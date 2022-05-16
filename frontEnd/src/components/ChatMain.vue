<template>
  <div class="chat-main-container">    
    <div class="chat-message-container" v-if="to_user_id">
      <h1>WebSocket Chat</h1>     
      <h2>Your ID: {{user_id}}</h2>
      <h2>Chat with user ID: {{to_user_id}}</h2>
      <div class="chat-input">
        <input v-model="message" placeholder="enter message" >
      </div>
      <div class="chat-button plus" v-on:click="sendMessage">Send</div>
      <div v-for="message in contentFilter" :key="message.user_id">
        <div>
          <p>{{message.message}}</p>
        </div>        
      </div>
    </div>
    <div class="chat-message-container" v-else>
      <h1 >WebSocket Chat</h1>
      <h2>Your ID: {{user_id}}</h2>
      <h2>Select user</h2>
    </div>
    <div class="chat-right-dashboard" v-if="users.length!==0">      
      <ChatUserButton 
        v-for="user in users" 
        :key="user.id" 
        :user="user"
        v-on:seleckUser="seleckUser"
      />    
    </div>
    <div class="chat-right-dashboard" v-else>
      <h2>There are no users here</h2>
    </div>
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'
import ChatUserButton from './ChatUserButton'
import {mapMutations} from 'vuex'

export default {
  name: 'ChatMain',
  components: {
    ChatUserButton
  },
  data(){
    return {
      connection: null,
      content:[],
      users: [],
      message:'',
      user_id: uuidv4(),
      to_user_id:''
    }
  },
  computed: {    
    contentFilter(){
      return this.content.filter((item) => {              
          const check_to = item.to_id === this.to_user_id
          const check_from = item.from_id === this.to_user_id         
          return check_to || check_from
        })
    }    
  },
  mounted() {
    this.webSocket()
  },
  methods: {
    ...mapMutations(["SET_NODES_TO_STATE", "SET_LINKS_TO_STATE", "SET_CHART_ACTION_MESSAGE"]),
  
    sendMessage(){
     
      const message_data = {
        message: this.message,
        to_user_id: this.to_user_id
      }
      this.connection.send(JSON.stringify({message_data}))
      this.message = ''
    },
    seleckUser(selec_id){
      this.users.map((item)=>{
        if (item.id === this.to_user_id){          
          item.seleckt = false         
        } 
        if (item.id === selec_id){
          item.seleckt = true         
        }
      })
      this.to_user_id = selec_id
    },
   
    webSocket(){     
      const _this = this     
      _this.connection = new WebSocket(`ws://localhost:8000/ws/${this.user_id}`)
      _this.connection.onmessage = function(event) {        
        const data = JSON.parse(event.data)        
        
        if (data.type_action === 'message'){
          _this.content.push(data)
        }

        if (data.type_action === 'users-add'){
          _this.users.push(data.users)
        }

        if (data.type_action === "users-create"){
          _this.users = data.users
        }

        if (data.type_action === 'users-delet'){
          
          _this.users.map((item,i)=>{
            if (item.id === data.users_delet.id){
              _this.users.splice(i, 1)
            }
          })

          _this.content = _this.content.filter((item) => {              
            const check_to = item.to_id !== data.users_delet.id
            const check_from = item.from_id !== data.users_delet.id         
            return check_to || check_from
          })

          if (data.users_delet.id === this. to_user_id) this. to_user_id = ''

        }

        if (data.type_action === 'chart_send_message'){
          _this.SET_NODES_TO_STATE(data.nodes)
          _this.SET_LINKS_TO_STATE(data.links)
          _this.SET_CHART_ACTION_MESSAGE(data.link_update_id)    
       
        }

        if (data.type_action === 'chart_add_node'){
          _this.SET_NODES_TO_STATE(data.nodes)
          _this.SET_LINKS_TO_STATE(data.links)
        }

        if (data.type_action === 'chart_delete_node'){
          _this.SET_NODES_TO_STATE(data.nodes)
          _this.SET_LINKS_TO_STATE(data.links)
        }
      }
    }
  }
}
</script>

<style>
.chat-main-container{
  display: flex;
  margin: 2rem;
  flex-direction: row;
  width: 50%;
}
.chat-message-container{
  display: flex;
  flex-direction: column;
  width: 70%;
  align-items: center;
  padding: 3rem;
  box-shadow: 2px 2px 15px 2px rgba(0, 0, 0, 0.1);
}
.chat-right-dashboard{
  flex-direction: row;
  width: 30%;
  box-shadow: 2px 2px 15px 2px rgba(0, 0, 0, 0.1);
}
.chat-button {  
  width: 100%;
  padding: 1rem;
  border: medium solid;    
}
.plus {
  color: green;
}
.chat-chat{
  flex-direction: row;
}
input {
  min-width: 100%;
  max-width: 100%;
  border-radius:10px;
  padding: 1rem; 
  box-sizing: border-box;
}
.chat-input{
  width: 100%;
  margin: 2rem;
}
</style>
