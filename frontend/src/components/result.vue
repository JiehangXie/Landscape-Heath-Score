<template>
      <el-row type="flex" class="row-bg" justify="center">
          <el-col :span="12">
              <el-card class="box-card" :body-style="{ padding: '0px' }">
                <template #header>
                  <div class="card-header">
                    <span>Image Segmentation</span>
                    <el-tooltip class="item" effect="dark" content="The program is being tested and the results are for reference only." placement="right">
                      <i class="el-icon-warning-outline" style="margin-left:10px;"></i>
                    </el-tooltip>
                  </div>
                </template>
                <div>
                  <div class="block">
                    <el-image :src="image" style="width:100%;height:600px;" :fit="scale-down" :preview-src-list="preview_image">>
                    <template #placeholder>
                      <div class="image-slot">
                        Loading……<span class="dot">...</span>
                      </div>
                    </template>
                    </el-image>
                    <div style="padding: 14px;text-align:center;">
                       <a :href="image" download="seg.png" style=”color:#fff;text-decoration:none;“><el-button type="success" size="medium" class="button"><i class="el-icon-download">Download</i></el-button></a>
                    </div>
                  </div>
                </div>
              </el-card>
          </el-col>
          </el-row>

          <el-row type="flex" class="row-bg" justify="center" style="margin-top:30px">
            <el-col :span="12">
              <el-card class="box-card" shadow="hover">
                <template #header>
                  <div class="card-header">
                    <span>Result</span> 
                  </div>
                </template>
                  <el-row type="flex" class="row-bg" justify="center">
                    <div id="seg-bar" :style="{ width: '800px', height: '300px' }"></div>
                  </el-row>
                  <el-row type="flex" class="row-bg" justify="center">
                    <el-col :span="12" class="main-emotion">
                      <div id="totalscore" :style="{width: '430px',height: '430px'}"></div>
                    </el-col>
                    <el-col :span="12">
                      <div id="qscore" :style="{width: '350px',height: '300px'}"></div>
                    </el-col>

                  </el-row>

              </el-card>
            </el-col>
          </el-row>

          <el-row type="flex" class="row-bg" justify="center" style="margin-top:15px">
                <a href="../"><el-button type="success" size="medium" class="button"><i class="el-icon-back"> Change another one</i></el-button></a>
          </el-row>
</template>

<script>
  import * as echarts from 'echarts';
  import { onMounted } from 'vue';
  export default {
      data() {
        return {
          activeIndex: '1',
          activeIndex2: '2',
          image:'',
          preview_image:[],
          gvr:0.0,
          proportion:Array(),
          score:Array()
        };
      },
      mounted(){
        var json_result = JSON.parse(this.$route.params.json_result);
        var score_list = JSON.parse(json_result['score'])
        this.image = 'data:image/jpg;base64,' + json_result['image'];
        this.preview_image = [this.image]
        this.proportion = JSON.parse(json_result['proportion']);
        this.gvr = json_result['gvr'];
        this.score = Array(score_list['relaxed'],score_list['happy'],score_list['focused'],score_list['motivated'],score_list['social'],score_list['depressive']);
        this.proportion_bar();
        this.gvr_render();
        this.radar();
      },

      methods: {
        proportion_bar(){
          var SegchartDom = document.getElementById('seg-bar');
          var Segbar = echarts.init(SegchartDom);
          var Seg_option;

          Seg_option = {
              title: {
                text: 'Proportion of Landscape Elements',
                x:'center',
                y:'top',
                textAlign:'left',
                  },
              tooltip: {
                  trigger: 'axis',
                  axisPointer: {
                      type: 'shadow'
                  }
              },
              yAxis: {
                  type: 'category',
                  data: ['Others', 'Road', 'Sidewalk', 'Building', 'Wall', 'Fence', 'Pole', 'Vegetation', 'Terrain', 'Sky'],
                  axisLabel: {  
                    interval:0,  
                    rotate:0  
                  }  
              },
              xAxis: {
                  type: 'value'
              },
              
              series: [{
                  data: [{ value: this.proportion['others'], itemStyle: { color: 'rgb(64,0,128)' }}, 
                        { value: this.proportion['road'], itemStyle: { color: 'rgb(128,0,0)' }}, 
                        { value: this.proportion['sidewalk'], itemStyle: { color: 'rgb(0,128,0)' }}, 
                        { value: this.proportion['building'], itemStyle: { color: 'rgb(128,128,0)' }}, 
                        { value: this.proportion['wall'], itemStyle: { color: 'rgb(0,0,128)' }}, 
                        { value: this.proportion['fence'], itemStyle: { color: 'rgb(128,0,128)' }}, 
                        { value: this.proportion['pole'], itemStyle: { color: 'rgb(0,128,128)' }}, 
                        { value: this.proportion['vegetation'], itemStyle: { color: 'rgb(192,0,0)' }}, 
                        { value: this.proportion['terrain'], itemStyle: { color: 'rgb(64,128,0)' }}, 
                        { value: this.proportion['sky'], itemStyle: { color: 'rgb(192,128,0)' }}],
                  type: 'bar',
                  showBackground: true,
                  backgroundStyle: {
                      color: 'rgba(180, 180, 180, 0.2)'
                  }
              }],
              grid: {
                top: "15%",
                left: "0%",
                right: "0%",
                bottom: "10%",
                containLabel: true,
              },
          };

          Seg_option && Segbar.setOption(Seg_option);
        },

        gvr_render(){
          var gvr_chartDom = document.getElementById('totalscore');
          var gvr_Chart = echarts.init(gvr_chartDom);
          var gvr_option;

          gvr_option = {
              series: [{
                  type: 'gauge',
                  startAngle: 180,
                  endAngle: 0,
                  min: 0,
                  max: 1,
                  splitNumber: 8,
                  axisLine: {
                      lineStyle: {
                          width: 8,
                          color: [
                              [0.15, '#FF6E76'],
                              [0.25, '#FDDD60'],
                              [1, '#91CC75'],
                          ]
                      }
                  },
                  pointer: {
                      icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                      length: '12%',
                      width: 20,
                      offsetCenter: [0, '-60%'],
                      itemStyle: {
                          color: 'auto'
                      }
                  },
                  axisTick: {
                      length: 12,
                      lineStyle: {
                          color: 'auto',
                          width: 2
                      }
                  },
                  splitLine: {
                      length: 20,
                      lineStyle: {
                          color: 'auto',
                          width: 2
                      }
                  },
                  axisLabel: {
                      color: '#464646',
                      fontSize: 12,
                      distance: -70,
                      formatter: function (value) {
                          if (value === 0.5) {
                              return '';
                          }
                          else if (value === 0.25) {
                              return '';
                          }
                          else if (value === 0.125) {
                              return '';
                          }
                      }
                  },
                  title: {
                      offsetCenter: [0, '-20%'],
                      fontSize: 18
                  },
                  detail: {
                      fontSize: 30,
                      offsetCenter: [0, '0%'],
                      valueAnimation: true,
                      formatter: function (value) {
                          return Math.round(value * 100) + '%';
                      },
                      color: 'auto'
                  },
                  data: [{
                      value: this.gvr,
                      name: 'Green Vision Rate'
                  }]
              }]
          };

          gvr_option && gvr_Chart.setOption(gvr_option);

        },

        radar(){
          var Qscore_chartDom = document.getElementById('qscore');
          var Qscore = echarts.init(Qscore_chartDom);
          var Qscore_option;

          Qscore_option = {
              tooltip: {
                  
              },
              radar: {
                  // shape: 'circle',
                  indicator: [
                      { name: 'Relaxed', max: 10},
                      { name: 'Happy', max: 10},
                      { name: 'Focused', max: 10},
                      { name: 'Motivated', max: 10},
                      { name: 'Social', max: 10},
                      { name: 'Depressive', max: 10}
                  ]
              },
              
              series: [{
                  name: 'Emotion',
                  type: 'radar',
                  data: [
                      {
                          value: this.score,
                          name: 'Emotion'
                      },
                  ]
              }]
          };

          Qscore_option && Qscore.setOption(Qscore_option);
        },
      }





  }
</script>

<style>

.el-card{
  height:730px;
}
.main-emotion{
  margin:auto;
}
#seg-bar{
  margin:auto;
}
#qscore{
  margin: auto;
}

</style>
