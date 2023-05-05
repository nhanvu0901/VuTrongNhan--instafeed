import {createApp, h} from 'vue/dist/vue.esm-bundler';
import App from './App.vue'
import 'ant-design-vue/dist/antd.css';
import Antd from 'ant-design-vue';
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { far } from '@fortawesome/free-regular-svg-icons';
import {faInstagram,faFacebook,} from "@fortawesome/free-brands-svg-icons";
import {faComment} from "@fortawesome/free-solid-svg-icons";
library.add(fas, far,faInstagram,faFacebook,faComment)
let widget_list = document.querySelectorAll(".instagram-odoo-mint")
for (let i = 0; i < widget_list.length; i++){
}
    if (widget_list.length > 0) {
        for (let widget_element of widget_list) {
            let hashed_id = widget_element.getAttribute('data-widget-id')
            let app = createApp({
                name: 'Widget_' + hashed_id,
                render: () => h(App, {data: {widget_id: hashed_id}})
            })
            app.component("font-awesome-icon", FontAwesomeIcon).use(Antd).mount(widget_element)
        }
    }

