<script setup lang="ts">
import { ref } from "vue"
import { ElMessageBox } from "element-plus"
import type { UploadProps, UploadUserFile, UploadFile } from "element-plus"

const fileList = ref<UploadUserFile[]>([])
const dialogVisible = ref(false)
const dialogImageUrl = ref("")

const handleRemove: UploadProps["onRemove"] = (file, uploadFiles) => {
    console.log(file, uploadFiles)
}

const beforeRemove: UploadProps["beforeRemove"] = (uploadFile, uploadFiles) => {
    return ElMessageBox.confirm(
        `Cancel the transfert of ${uploadFile.name} ?`
    ).then(
        () => true,
        () => false
    )
}

const getPath =  (file:UploadFile):string => {
    const task_id = file.response.result.image.task_id
    const id = file.response.result.image.id
    return `http://localhost:5010/static/task/${task_id}/${id}.jpg`
}
</script>

<template>
    <el-upload
        action="http://localhost:5010/upload_image"
        name="uploadFile"
        :on-remove="handleRemove"
        :before-remove="beforeRemove"
        :file-list="fileList"
        multiple
    >
        <el-button type="primary">アップロード</el-button>
        <template #tip>
            <div class="el-upload__tip">
                jpg/png files with a size less than 500KB.
            </div>
        </template>
    </el-upload>
    <el-row v-if="fileList.length > 0">
    <el-col
      v-for="(file, index) in fileList"
      :key="index"
      :span="8"
    >
      <el-card>
        <img
          :src=getPath(file)
          class="image"
        />
      </el-card>
    </el-col>
  </el-row>
</template>
<style scoped>
.image {
  width: 100%;
  display: block;
}
</style>