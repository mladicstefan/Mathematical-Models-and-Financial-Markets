#include <SDL2/SDL.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

const int WIDTH = 800;
const int HEIGHT = 600;

typedef struct {
  double m1,m2;
  double l1,l2;
  double a1,a2;
  double a1_v,a2_v;
}DoublePendulum;

double g = 9.81;

typedef struct {
  double da1;
  double da2;
  double dv1;
  double dv2;
} State;

State derivatives (const DoublePendulum *p){

    double m1 = p->m1;
    double m2 = p->m2;
    double l1 = p->l1;
    double l2 = p->l2;
    double a1 = p->a1;
    double a2 = p->a2;
    double v1 = p->a1_v;  
    double v2 = p->a2_v;
    
    // Compute angular acceleration for first pendulum (α1)
    double num1 = -g*(2*m1 + m2)*sin(a1);
    double num2 = -m2*g*sin(a1 - 2*a2);
    double num3 = -2*m2*sin(a1 - a2);
    double num4 = v2*v2*l2 + v1*v1*l1*cos(a1 - a2);
    double den  = l1*(2*m1 + m2 - m2*cos(2*(a1 - a2)));
    double a1_a = (num1 + num2 + num3 * num4) / den;
    
    // angular accel for second pendulum(α2)
    num1 =  2*sin(a1 - a2);
    num2 =  v1*v1*l1*(m1 + m2);
    num3 =  g*(m1 + m2)*cos(a1);
    num4 =  v2*v2*l2*m2*cos(a1 - a2);
    den   =  l2*(2*m1 + m2 - m2*cos(2*(a1 - a2)));
    double a2_a = (num1 * (num2 + num3 + num4)) / den;

    return (State){
    .da1 = v1,
    .da2 = v2,
    .dv1 = a1_a,
    .dv2 = a2_a
  };

}

void rk4_step(DoublePendulum *p, double dt) {
    // 1) Compute k1 using current state
    State s1 = derivatives(p);

    // 2) Compute state at midpoint using k1/2
    DoublePendulum p2 = *p;
    p2.a1   += s1.da1 * dt/2;
    p2.a2   += s1.da2 * dt/2;
    p2.a1_v += s1.dv1  * dt/2;
    p2.a2_v += s1.dv2  * dt/2;
    State s2 = derivatives(&p2);

    // 3) Compute state at midpoint using k2/2
    DoublePendulum p3 = *p;
    p3.a1   += s2.da1 * dt/2;
    p3.a2   += s2.da2 * dt/2;
    p3.a1_v += s2.dv1  * dt/2;
    p3.a2_v += s2.dv2  * dt/2;
    State s3 = derivatives(&p3);

    // 4) Compute state at end using k3
    DoublePendulum p4 = *p;
    p4.a1   += s3.da1 * dt;
    p4.a2   += s3.da2 * dt;
    p4.a1_v += s3.dv1  * dt;
    p4.a2_v += s3.dv2  * dt;
    State s4 = derivatives(&p4);

    // Combine increments: p_new = p + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
    p->a1   += dt * (s1.da1 + 2*s2.da1 + 2*s3.da1 + s4.da1) / 6;
    p->a2   += dt * (s1.da2 + 2*s2.da2 + 2*s3.da2 + s4.da2) / 6;
    p->a1_v += dt * (s1.dv1  + 2*s2.dv1  + 2*s3.dv1  + s4.dv1) / 6;
    p->a2_v += dt * (s1.dv2  + 2*s2.dv2  + 2*s3.dv2  + s4.dv2) / 6;
}

int main(int argc, char *argv[]) {

  if (SDL_Init(SDL_INIT_VIDEO) < 0) {
    fprintf(stderr, "SDL_Init Error: %s\n", SDL_GetError());
    exit(1);
  }

  SDL_Window *win = SDL_CreateWindow(
    "Double Pendulum",
    SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
    WIDTH, HEIGHT,
    0
  );
  if (!win) {
    fprintf(stderr, "SDL_CreateWindow Error: %s\n", SDL_GetError()); 
    SDL_Quit();
    exit(1);
    }
  
  SDL_Renderer *ren = SDL_CreateRenderer(win,-1,SDL_RENDERER_ACCELERATED);
  
  if (!ren) {
      fprintf(stderr, "SDL_CreateRenderer Error: %s\n", SDL_GetError());
      SDL_DestroyWindow(win);
      SDL_Quit();
      exit(1);
  }

  SDL_SetRenderDrawBlendMode(ren, SDL_BLENDMODE_BLEND);
  SDL_SetRenderDrawColor(ren, 0, 0, 0, 255);
  SDL_RenderClear(ren);
  
  const int N = 3;
  DoublePendulum ps[N];

  double base_angle = M_PI/2;  // 90° from vertical
  double delta      = 0.01;    // small difference for chaos
  for (int i = 0; i < N; i++) {
        ps[i].m1 = ps[i].m2 = 10;        // equal masses
        ps[i].l1 = ps[i].l2 = 150;       // equal lengths
        ps[i].a1 = base_angle + i * delta; // stagger initial angles
        ps[i].a2 = base_angle + i * delta;
        ps[i].a1_v = ps[i].a2_v = 0;     // start at rest
  }

  double dt = 0.01;
  SDL_Event e;

  while (1) {
    
    while (SDL_PollEvent(&e)) {
      if (e.type == SDL_QUIT) goto cleanup;
    }
    
    SDL_SetRenderDrawColor(ren, 0, 0, 0, 15);
    SDL_RenderFillRect(ren,NULL);

    for (int i = 0; i < N; i++){

      rk4_step(&ps[i], dt);
      double x1 = WIDTH/2 + ps[i].l1 * sin(ps[i].a1);
      double y1 = HEIGHT/4 + ps[i].l1 * cos(ps[i].a1);
      double x2 = x1 + ps[i].l2 * sin(ps[i].a2);
      double y2 = y1 + ps[i].l2 * cos(ps[i].a2);
      
      Uint8 r = (i == 0) ? 255 : 0;
      Uint8 g = (i == 1) ? 255 : 0;
      Uint8 b = (i == 2) ? 255 : 0;    

      SDL_SetRenderDrawColor(ren, r, g, b, 255);
      SDL_RenderDrawPoint(ren, (int)x2, (int)y2);

  
      SDL_SetRenderDrawColor(ren, r, g, b, 255);
      SDL_RenderDrawLine(ren, WIDTH/2, HEIGHT/4, (int)x1, (int)y1);
      SDL_RenderDrawLine(ren, (int)x1, (int)y1, (int)x2, (int)y2);

    
      SDL_Rect bob1 = {(int)x1 - 5, (int)y1 - 5, 10, 10};
      SDL_Rect bob2 = {(int)x2 - 5, (int)y2 - 5, 10, 10};
      SDL_RenderFillRect(ren, &bob1);      
      SDL_RenderFillRect(ren, &bob2);
      
    }
      SDL_RenderPresent(ren);
  }
  cleanup:
    SDL_DestroyRenderer(ren);
    SDL_DestroyWindow(win);
    SDL_Quit();
    return 0;


}
