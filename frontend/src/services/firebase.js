import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey: "AIzaSyCS2vu2isJK6E-PPuAWjPDZ-QDWUlNJXS0",
  authDomain: "rewind-95f1b.firebaseapp.com",
  projectId: "rewind-95f1b",
  storageBucket: "rewind-95f1b.firebasestorage.app",
  messagingSenderId: "823218795423",
  appId: "1:823218795423:web:1dd0742d573cc03b20c3aa",
  measurementId: "G-T2M838X5HK"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);
export const googleProvider = new GoogleAuthProvider();

export const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    return result.user;
  } catch (error) {
    console.error('Google sign-in error:', error);
    throw error;
  }
};

export const logout = async () => {
  try {
    await signOut(auth);
  } catch (error) {
    console.error('Logout error:', error);
    throw error;
  }
};

export { onAuthStateChanged };
