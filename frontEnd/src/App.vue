<template>
  <div id="app">
    <div class="contener">
      <ChatMain/>      
      <D3ForsGraph/>
    </div>
  </div> 
  
</template>

<script>
import ChatMain from './components/ChatMain'
import D3ForsGraph from './components/D3ForsGraph'

export default {
  name: 'App',
  components: { D3ForsGraph, ChatMain},
  data(){
    return {
 
    }
  },  
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.contener{
  display: flex;
  margin-left: 2rem;
  margin-right: 2rem;
  min-height: 90vh;
}
.chart-container{
  margin: 2rem;
  width: 50%;
}
</style>
