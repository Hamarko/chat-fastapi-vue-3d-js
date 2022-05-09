<template>
  
  <div id="containerGraph" class="chart-container">
    <svg xmlns="http://www.w3.org/2000/svg" 
         :width="width"
         :height="height"
         @mousemove="drag($event)"
         @mouseup="drop()"
         v-if="bounds.minX">
      <defs>       
          <marker id="m-end" markerWidth="10" markerHeight="10" refX="15" refY="0" 
                  orient="auto" 
                  markerUnits="strokeWidth" 
                  viewBox="0 -5 10 10" >
            <path d="M0,-5L10,0L0,5"></path>
          </marker>        
      </defs>
      <transition-group tag="g" name="line">
        <line v-for="link in graph.links"
              :x1="coords[link.source.index].x"
              :y1="coords[link.source.index].y"
              :x2="coords[link.target.index].x"
              :y2="coords[link.target.index].y"
              stroke="black" stroke-width="2"
              :key="link.source.index"
              marker-end="url(#m-end)"
              :id="link.source.id"
              class="activet"
              />
      </transition-group>
      <transition-group tag="g" name="circle">
        <circle v-for="(node, i) in graph.nodes"
                class="bounce-enter-active"
                :cx="coords[i].x"
                :cy="coords[i].y"
                :r="10" :fill="colors[Math.ceil(Math.sqrt(node.index))]"
                stroke="white" stroke-width="1"
                @mousedown="currentMove = {x: $event.screenX, y: $event.screenY, node: node}"
                :key="i"
                />
      </transition-group>
     
      <text v-for="(node, i) in graph.nodes"
            :key="i"
            :x="coords[i].x -25"
            :y="coords[i].y-10"
      >{{node.id}}</text>
    </svg>
  </div>
</template>

<script>
import * as d3 from "d3"
import {mapGetters} from 'vuex'



export default {
  name: 'D3ForsGraph',
  data(){
    return {     
      width: 500,
      height: 600,
      padding: 50,
      colors: ['#2196F3', '#E91E63', '#7E57C2', '#009688', '#00BCD4', '#EF6C00', '#4CAF50', '#FF9800', '#F44336', '#CDDC39', '#9C27B0'],
      simulation: null,
      currentMove: null
    }
   
  },
  computed: {
    ...mapGetters(["nodes", "links", "sendMessageAction", "linkIndexAction"]),
    graph:{
      get(){
        return{
          nodes: this.nodes,
          links: this.links
        }
      },
      set(newValue){
        this.nodes = newValue.nodes
        this.links = newValue.links
        this.SET_NODES_TO_STATE(this.nodes)
        this.SET_LINKS_TO_STATE(this.links)
      }
    },
    bounds() {
      return {
        minX: Math.min(...this.graph.nodes.map(n => n.x)),
        maxX: Math.max(...this.graph.nodes.map(n => n.x)),
        minY: Math.min(...this.graph.nodes.map(n => n.y)),
        maxY: Math.max(...this.graph.nodes.map(n => n.y))
      }
    },

    coords() {
      return this.graph.nodes.map(node => {
        let x = this.padding + (node.x - this.bounds.minX) * (this.width - 5*this.padding) / (this.bounds.maxX - this.bounds.minX)
        let y = this.padding + (node.y - this.bounds.minY) * (this.height - 5*this.padding) / (this.bounds.maxY - this.bounds.minY)
        if (isNaN(x)) x = 100
        if (isNaN(y)) y = 100
        return {x, y}
      })
    }
  },
  created(){
    this.startSimulation(this.graph)
    
  },  
  watch: {
    graph(newGraph){
      this.startSimulation(newGraph)
    }

  },
  methods: {        
    drag(e) {
      if (this.currentMove) {
        this.currentMove.node.fx = this.currentMove.node.x - (this.currentMove.x - e.screenX) * (this.bounds.maxX - this.bounds.minX) / (this.width - 2 * this.padding)
        this.currentMove.node.fy = this.currentMove.node.y -(this.currentMove.y - e.screenY) * (this.bounds.maxY - this.bounds.minY) / (this.height - 2 * this.padding)
        this.currentMove.x = e.screenX
        this.currentMove.y = e.screenY
      }
    },
    drop(){      
      if(this.currentMove){
        delete this.currentMove.node.fx
        delete this.currentMove.node.fy    
        this.currentMove = null
        this.simulation.alpha(1)
        this.simulation.restart()
      }
    },
    startSimulation(newGraph){
      this.simulation = d3.forceSimulation(newGraph.nodes)
       /* eslint-disable */ 
       .force('charge', d3.forceManyBody().strength(d => -10))
       .force('link', d3.forceLink(newGraph.links).id(d => d.id))
       .force('x', d3.forceX())
       .force('y', d3.forceY())      
    }    
  }
}
</script>
<style>

text {
  font: 12px sans-serif;
  pointer-events: none;
  text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;
}
.bounce-enter-active {
  animation: bounce-in 1s;
}
.bounce-leave-active {
  animation: bounce-in 1s reverse;
}
.activet{
  animation-name: example;
  animation-duration: 2s;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
  
}
@keyframes example {
  from {stroke: black;}
  to {stroke: green;}  
}

</style>