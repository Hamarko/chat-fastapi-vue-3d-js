<template>
  <div class="user-button" :class="{plus: user.seleckt}" @click="seleckUser">
    <p>{{user.id}}</p>
  </div>
</template>

<script>
export default {
  name: 'ChatUserButton',
  props: {
    user: Object
  },
  methods: {
    seleckUser(){
      this.$emit('seleckUser', this.user.id)
      this.selecktClick = true
    }
  }
}
</script>

<style>
.user-button{
  padding: 1rem;
  border: medium solid;  
} 
.plus {
  color: green;
}   
</style>