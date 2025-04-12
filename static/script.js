// static/script.js
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("uploadForm");
    const downloadSection = document.getElementById("downloadSection");
    const downloadLink = document.getElementById("downloadLink");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // 폼 기본 동작(페이지 새로고침) 방지

        const formData = new FormData(form);

        try {
            const response = await fetch("/convert", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error("변환 실패! 다시 시도해주세요.");
            }

            const blob = await response.blob();
            const objectUrl = URL.createObjectURL(blob);

            downloadLink.href = objectUrl;
            downloadLink.download = "converted.zip"; // 변환된 이미지 파일이 zip 형태라고 가정
            downloadSection.style.display = "block";
        } catch (
