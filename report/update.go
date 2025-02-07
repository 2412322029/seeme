package main

import (
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
)

func main() {
	if len(os.Args) != 4 {
		fmt.Println("Usage: update <source_dir> <target_dir> <pid>")
		os.Exit(1)
	}

	sourceDir := os.Args[1] // 源目录
	targetDir := os.Args[2] // 目标目录
	pidStr := os.Args[3]    // 进程ID

	pid, err := strconv.Atoi(pidStr)
	if err != nil {
		fmt.Printf("无效的PID：%s\n", pidStr)
		os.Exit(1)
	}

	process, err := os.FindProcess(pid)
	if err != nil {
		fmt.Printf("未找到PID为%d的进程：%v\n", pid, err)
		fmt.Println("跳过终止进程操作，继续后续步骤...")
	} else {
		if err := process.Kill(); err != nil {
			fmt.Printf("终止PID为%d的进程失败：%v\n", pid, err)
			os.Exit(1)
		}
		fmt.Printf("PID为%d的进程已被终止。\n", pid)
	}

	err = copyDir(sourceDir, targetDir)
	if err != nil {
		fmt.Printf("从%s复制文件到%s失败：%v\n", sourceDir, targetDir, err)
		os.Exit(1)
	}
	fmt.Printf("文件已从%s成功复制到%s。\n", sourceDir, targetDir)


	reportExePath := filepath.Join(targetDir, "report.exe")
	cmd := exec.Command(reportExePath)
	if err := cmd.Start(); err != nil {
		fmt.Printf("启动report.exe失败：%v\n", err)
		os.Exit(1)
	}
	fmt.Println("report.exe已启动。")
}

func copyDir(src, dst string) error {
	srcInfo, err := os.Stat(src)
	if err != nil {
		return err
	}

	if !srcInfo.IsDir() {
		return fmt.Errorf("源路径不是一个目录")
	}

	dstInfo, err := os.Stat(dst)
	if err != nil {
		if !os.IsNotExist(err) {
			return err
		}
		if err := os.MkdirAll(dst, srcInfo.Mode()); err != nil {
			return err
		}
	} else if !dstInfo.IsDir() {
		return fmt.Errorf("目标路径不是一个目录")
	}

	files, err := os.ReadDir(src)
	if err != nil {
		return err
	}

	for _, file := range files {
		srcPath := filepath.Join(src, file.Name())
		dstPath := filepath.Join(dst, file.Name())

		if file.IsDir() {
			if err := copyDir(srcPath, dstPath); err != nil {
				return err
			}
		} else {
			if err := copyFile(srcPath, dstPath); err != nil {
				return err
			}
		}
	}
	return nil
}


func copyFile(src, dst string) error {
	srcFile, err := os.Open(src)
	if err != nil {
		return err
	}
	defer srcFile.Close()

	dstFile, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer dstFile.Close()

	_, err = io.Copy(dstFile, srcFile)
	return err
}