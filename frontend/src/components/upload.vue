<template>
    <el-row type="flex" class="row-bg" justify="center" align="middle" style="margin-top:20px;">
      <el-col :span='12'>
        <h1 style="color:#555;font-weight: bold;font-size: 34px;text-align:center;">Landscape-Health Score</h1>
        <p style="color:#888;font-weight: bold;font-size: 21px;text-align:center;">A tool for evaluating landscape health benefits and supporting evidence-based design</p>
      </el-col>
    </el-row>

    <el-row type="flex" class="row-bg" justify="center" align="middle">
      <div class='container'>
        <div class='img background-img'></div>
        <div class='img foreground-img'></div>
        <input type="range" min="1" max="100" value="50" class="slider" name='slider' id="slider">
        <div class='slider-button'></div>
      </div>
    </el-row>
    <el-row style="margin-top:15px" type="flex" class="row-bg" justify="center" align="middle">
      <el-button type="success" size="medium" class="button" @click="preview_box">Preview</el-button>
    </el-row>
    <el-row style="margin-top:15px" type="flex" class="row-bg" justify="center" align="middle">
        <h3 style="color:#888;font-weight: bold;font-size: 20px;text-align:center;">Upload Your Own Image</h3>
    </el-row>
    <el-row style="margin-top:15px;" type="flex" class="row-bg" justify="center">

          <el-col :span="12">

                <el-row class="upload-box" type="flex" justify="center" align="middle">
                      <el-upload class="upload" 
                      drag 
                      action="http://127.0.0.1:5000/api/v1/file" 
                      limit=1
                      accept=".jpg,.jpeg,.png,.JPG,.JPEG,.PNG"
                      :on-progress="upload_process"
                      :on-success="upload_success"
                      :on-error="on-error"
                      >
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">Drag the image here,or <em>Click this</em></div>

                        </el-upload>
                </el-row>

          </el-col>
      </el-row>

</template>

<script>

 import { ElMessage } from 'element-plus'
  export default{
    data(){
      return {
      }
    },
    mounted(){
      const slider = document.getElementById("slider");
      let sliderPos
      slider.addEventListener("input", function(e){
        sliderPos = e.target.value
        document.querySelector(".foreground-img").style.width = `${sliderPos}%`
        document.querySelector(".slider-button").style.left = `calc(${sliderPos}% - 18px)`
      });

    },
    methods:{
      preview_box() {
        this.$alert('<img src="https://gitee.com/xiejiehang/Landscape-Heath-Score/raw/main/docs/demo_result.png">', 'Preview', {
          dangerouslyUseHTMLString: true,
          customClass: 'winClass',//弹窗样式
        });
      },
      upload_process() {
          ElMessage('Processing, please wait for a moment.');
        },
      upload_error(){
          ElMessage.error('There was an error occured!');
      },
      upload_success(response){
        ElMessage.success({
            message: 'Processing completed!',
            type: 'success'
          });
        this.$router.push({
            name:'result',
            params:{
              json_result:JSON.stringify(response)
            }
        })
            
      }
    }
  }
</script>

<style>
.container {
  margin-top:15px;
  position: relative;
  width: 900px;
  height: 600px;
}
.img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: 900px 100%;
}
.background-img {
  background-image: url('../assets/demo.jpg');
}
.foreground-img {
  background-image: url('../assets/demo.png');
  width: 50%;
}

.slider {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 100%;
  background: rgba(242,242,241,.3);
  outline: none;
  margin: 0;
  transition: all .2s;
}
.slider:hover {
  background: rgba(242,242,241,.1); 
}
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 0px;
  height: 600px;
  background: white;
}
.slider-button {
  pointer-events: none;
  position: absolute;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: white;
  left: calc(50% - 18px);
  top: calc(50% - 18px);
  display: flex;
  justify-content: center;
  align-items: center;
}
.slider-button::after {
  content: '';
  padding: 3px;
  display: inline-block;
  border: solid #5D5D5D;
  border-width: 0 2px 2px 0;
  transform: rotate(-45deg);
}
.slider-button::before {
  content: '';
  padding: 3px;
  display: inline-block;
  border: solid #5D5D5D;
  border-width: 0 2px 2px 0;
  transform: rotate(135deg);
}

.el-card{
    height:400px;
}
.el-upload-dragger{
  width:800px;
  height:400px;
}
.el-upload-dragger .el-icon-upload{
  margin: 20% 0 16px;
}
.winClass{
  width:850px;
}
</style>