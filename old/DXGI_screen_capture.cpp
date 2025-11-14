#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <d3d11.h>
#include <dxgi1_2.h>
#include <memory>
#include <stdio.h>

namespace py = pybind11;

#pragma comment(lib, "d3d11.lib")
#pragma comment(lib, "dxgi.lib")

DXGI_OUTDUPL_FRAME_INFO dupframeinfo{};
IDXGIResource* res = nullptr;
ID3D11Texture2D* pTmpTex = nullptr;
IDXGISurface1* pSurface = nullptr;
DXGI_MAPPED_RECT map;
D3D11_TEXTURE2D_DESC desc{};

ID3D11Device* d3d11;
ID3D11DeviceContext* d3d11context;
IDXGIOutputDuplication* pDup;
ID3D11Texture2D* pTex;

// CPU 접근용 텍스처 생성
static ID3D11Texture2D* CreateTexture(ID3D11Device* d3d11, int width, int height, DXGI_FORMAT colorformat) {
    D3D11_TEXTURE2D_DESC td{};
    td.Width = width;
    td.Height = height;
    td.MipLevels = 1;
    td.ArraySize = 1;
    td.Format = colorformat;
    td.SampleDesc.Count = 1;
    td.Usage = D3D11_USAGE_STAGING;
    td.CPUAccessFlags = D3D11_CPU_ACCESS_READ;
    ID3D11Texture2D* tex = nullptr;
    if (FAILED(d3d11->CreateTexture2D(&td, nullptr, &tex))) return nullptr;
    return tex;
}

void init() {
    IDXGIFactory1* pFactory;
    IDXGIAdapter* pAdapter;
    IDXGIOutput* pOut;
    DXGI_OUTPUT_DESC outdesc;
    IDXGIOutput1* pOut1;
    
    DXGI_OUTDUPL_FRAME_INFO dupframeinfo;
    IDXGIResource* res;
    ID3D11Texture2D * pTmpTex;
    IDXGIDevice1* pDxgiDev;
    //D3D11_TEXTURE2D_DESC texdesc;
    
    D3D_FEATURE_LEVEL fl = D3D_FEATURE_LEVEL_9_1;
    

    CreateDXGIFactory1(__uuidof(IDXGIFactory2), (void**)&pFactory); /*팩토리 생성*/
    pFactory->EnumAdapters(0, &pAdapter); /*만들어진 팩토리로 어댑터 얻기*/
    pAdapter->EnumOutputs(0, &pOut); /*어댑터에 물린 디스플레이 얻기 (여기선 0번 화면)*/
    pOut->GetDesc(&outdesc);
    pOut->QueryInterface(__uuidof(IDXGIOutput1), (void**)&pOut1); /*출력개체 확장 얻어오기*/

    /*d3d11 디바이스 및 컨텍스트 생성*/
    D3D11CreateDevice(pAdapter, D3D_DRIVER_TYPE_UNKNOWN, 0, 0, 0, 0, D3D11_SDK_VERSION, &d3d11, &fl, &d3d11context);
    d3d11->QueryInterface(__uuidof(IDXGIDevice1), (void**)&pDxgiDev); /*DXGI 인터페이스 얻어오기*/
    pOut1->DuplicateOutput(d3d11, &pDup); /*Duplicator 얻어오기*/
    pDup->AcquireNextFrame(16, &dupframeinfo, &res); /*현재 화면 프레임 얻어오기 (16ms 안에 얻어오기)*/
    res->QueryInterface(__uuidof(ID3D11Texture2D), (void**)&pTmpTex); /*얻어온 리소스는 텍스쳐로*/
    pTmpTex->GetDesc(&desc); /*화면 크기 등의 정보를 얻기 위함*/
    pDup->ReleaseFrame(); /*일단 다시 해제*/
    pTex = CreateTexture(d3d11, desc.Width, desc.Height, desc.Format); /*저 텍스쳐는 CPU가 바로 사용 할 수 없으므로 새로 만듬*/
}

// 전체 화면 이미지를 NumPy 배열로 가져오기
py::array get_screen_image() {

    // 프레임 획득
    if (FAILED(pDup->AcquireNextFrame(16, &dupframeinfo, &res))) {
        return py::array();  // 실패하면 빈 배열 반환
    }

    res->QueryInterface(__uuidof(ID3D11Texture2D), (void**)&pTmpTex);
    d3d11context->CopyResource(pTex, pTmpTex);

    pTex->QueryInterface(__uuidof(IDXGISurface1), (void**)&pSurface);
    
    pSurface->Map(&map, DXGI_MAP_READ);

    pTex->GetDesc(&desc);

    py::buffer_info bufinfo(
        map.pBits,
        sizeof(uint8_t),
        py::format_descriptor<uint8_t>::format(),
        3,
        std::vector<size_t>{desc.Height, desc.Width, 4},
        std::vector<size_t>{(size_t)map.Pitch, 4, 1}
    );

    py::array result(bufinfo);

    pSurface->Unmap();
    pSurface->Release();
    pTmpTex->Release();
    res->Release();
    pDup->ReleaseFrame();

    return result;
}

PYBIND11_MODULE(DXGI_screen_capture, m) {
    m.def("get_screen_image", &get_screen_image, "Get full screen image as numpy array");
    m.def("init", &init, "initialize module");
}
