import { createStore } from "vuex"

export const store = createStore({
  state:{
    nodes: [],
    links: [],
    sendMessageAction: false,
    linkIndexAction: undefined
  },
  mutations:{
    SET_NODES_TO_STATE(state, nodes){
      state.nodes = nodes
    },
    SET_LINKS_TO_STATE(state, links){
      state.links = links
    },
    SET_CHART_ACTION_MESSAGE(state, linkIndexAction){
      state.linkIndexAction = linkIndexAction
      state.sendMessageAction = !state.sendMessageAction
    }
  },
  getters:{
    nodes(state){
      return state.nodes
    },
    links(state){
      return state.links 
    },
    sendMessageAction(state){
      return state.sendMessageAction
    },
    linkIndexAction(state){
      return state.linkIndexAction
    }
  }
})